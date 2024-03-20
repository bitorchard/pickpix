from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.db.models import IntegerField
from django.db.models.functions import Cast

import traceback
import os
import pwd
import grp
import logging
import json
from .models import *
from random import randrange
from web3 import Web3
from PIL import Image
from PIL import ImageDraw
from datetime import datetime, timedelta
from pathlib import Path
from eth_account.messages import encode_structured_data

log = logging.getLogger(__name__)

CHAIN_ID = 43114
WEI_PER_AVAX = 10**18
MIN_PRICE = 0.1
MAX_PIXEL_INDEX = 2500
PROVIDER_URL = 'https://api.avax.network/ext/bc/C/rpc'
CONTRACT_JSON_FILE = 'pickpix/contract.json'
KEYS_JSON_FILE = 'pickpix/keys.json'
CACHED_VOUCHER_KEY = 'CACHED_VOUCHER'
SIGNING_DOMAIN = "Pixel-Voucher"
SIGNATURE_VERSION = "1"
CACHED_VOUCHER_EXPIRATION_SECS = 30*60


class Voucher:
    def __init__(self, uri, min_price):
        self.uri = uri
        self.min_price = min_price
        self.creation_date = datetime.now()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def to_signed_json(self):
        return {
            "minPrice" : self.min_price,
            "uri" : self.uri,
            "signature" : generate_signature(self.min_price, self.uri),
        }


def index(request):
    template = loader.get_template('pickpix/avax.html')
    context = {}
    check_latest_token2()
    return HttpResponse(template.render(context, request))


def token_price(request):
    token_price = MIN_PRICE
    try:
        obj = GlobalConfig.objects.get(name='token_cost')
        token_price = float(obj.value)
    except Pixel.DoesNotExist:
        pass
    return JsonResponse({'token_price' : token_price})


def random_free_pixel():
    return 1


def voucher(request):
    voucher = request.session.get(CACHED_VOUCHER_KEY)
    if voucher:
        if not voucher.creation_date + time_delta(seconds=CACHED_VOUCHER_EXPIRATION_SECS) < datetime.now():
            return voucher

        del request.session[CACHED_VOUCHER_KEY]

    min_price = MIN_PRICE
    try:
        token_cost = GlobalConfig.objects.get(name='token_cost')
        min_price = float(token_cost.value)
    except Pixel.DoesNotExist:
        pass
    voucher = Voucher(generate_ipns(), int(min_price*WEI_PER_AVAX))

    return JsonResponse(voucher.to_signed_json())


def generate_signature(min_price, ipns_uri):
    w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

    with open(CONTRACT_JSON_FILE) as f:
        contract_json = json.load(f)
    with open(KEYS_JSON_FILE) as f:
        keys_json = json.load(f)

    data = {
        "types" : {
            "EIP712Domain": [
                { "name": "name", "type": "string" },
                { "name": "chainId", "type": "uint256" },
            ],
            "NFTVoucher" : [
                { "name": "minPrice", "type": "uint256" },
            ],
        },
        "domain" : {
            "chainId": CHAIN_ID,
            "name": SIGNING_DOMAIN,
        },
        "primaryType": "NFTVoucher",
        "message" : {
            "minPrice" : min_price,
        }
    }

    signable = encode_structured_data(data)
    signed = w3.eth.account.sign_message(signable, keys_json['private_key'])

    return signed.signature.hex()


def generate_ipns():
    return "ipns:///TEST_IPNS"


def check_latest_token2():
    w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

    with open(CONTRACT_JSON_FILE) as f:
        contract_json = json.load(f)

    csum_address = Web3.toChecksumAddress(contract_json['address'])
    contract = w3.eth.contract(abi=contract_json['abi'], address=csum_address);

    live_last_token = contract.functions.lastToken().call()
    db_last_token = 0
    db_last_pixel = 0
    used_pixels = lcg_pixels(db_last_token, live_last_token, db_last_pixel)
    render_secret_image2(used_pixels)
    use_live_last_pixel = False
    # Remember the last token and pixel so we don't regenerate the same pixels
    if use_live_last_pixel:
        live_last_pixel = used_pixels[-1]
        GlobalConfig(name='last_token', value=str(live_last_token)).save()
        GlobalConfig(name='last_pixel', value=str(last_pixel)).save()

        try:
            db_last_token = int(GlobalConfig.objects.get(name='last_token'))
            if db_last_token == live_last_token:
                return
            db_last_pixel = int(GlobalConfig.objects.get(name='last_pixel'))
        except GlobalConfig.DoesNotExist, ValueError:
            db_last_token = 0
            db_last_pixel = 0
            render_secret_image2([])
            GlobalConfig(name='last_token', value=str(live_last_token)).save()
            GlobalConfig(name='last_pixel', value=str(last_pixel)).save()
        except:
            pass


def lcg_pixels(db_last_token, live_last_token, db_last_pixel):
    pixels = []
    last_pixel = db_last_pixel
    lcg_c_value = 6666
    a_big_prime = 50177
    max_pixels = 50176 # 224^2
    for t in range(db_last_token, live_last_token):
        last_pixel = (last_pixel + lcg_c_value) % a_big_prime
        if last_pixel >= max_pixels:
            last_pixel = (last_pixel + lcg_c_value) % a_big_prime
        pixels.append(last_pixel)
    log.info(pixels)
    return pixels;


def draw_mask(used_pixels, size=2050, rows=224, cols=224):
    mask_file = Path('static/pickpix/images/mask.jpg')
    if mask_file.is_file():
        overlay = Image.open(mask_file)
    else:
        overlay = draw_grid()

    grid_size = size / rows
    draw = ImageDraw.Draw(overlay)

    for p in used_pixels:
        x_coord = int((p % cols) * grid_size)
        y_coord = int(int(p / cols) * grid_size)
        draw.rectangle((x_coord, y_coord, int(x_coord+grid_size), int(y_coord+grid_size)), fill=0)

    overlay.save(mask_file)

    uid = pwd.getpwnam('steve')[2]
    gid = grp.getgrnam('www-data')[2]
    return overlay


def draw_grid(size=2050, rows=224, cols=224):
    grid_file = 'static/pickpix/images/grid.jpg'
    step_count = rows
    grid = Image.new(mode='L', size=(size, size), color=255)

    draw = ImageDraw.Draw(grid)
    y_start = 0
    y_end = grid.height
    step_size = grid.width / step_count

    for x in range(cols):
        line = ((int(x*step_size), y_start), (int(x*step_size), y_end))
        draw.line(line, fill="#ddd")

    x_start = 0
    x_end = grid.width

    for y in range(rows):
        line = ((x_start, int(y*step_size)), (x_end, int(y*step_size)))
        draw.line(line, fill="#ddd", width=1)

    del draw

    grid.save(grid_file)

    uid = pwd.getpwnam('steve')[2]
    gid = grp.getgrnam('www-data')[2]
    return grid


def render_secret_image2(used_pixels):
    secret_file_src = 'pickpix/secret_lake_mod.png'
    secret_file_render = 'static/pickpix/secret_img.jpg'

    secret = Image.open(secret_file_src)
    secret = secret.convert('RGBA')

    overlay = draw_mask(used_pixels)

    secret.paste(overlay, mask=overlay)
    secret = secret.convert('RGB')
    secret.save(secret_file_render)

    uid = pwd.getpwnam('steve')[2]
    gid = grp.getgrnam('www-data')[2]


def insert_new_token(token_data):
    token_owner = token_data['owner']
    token_ids = [token_data['tokenId']]
    tokens = PickToken.objects.filter(token_id__in=token_ids)
    for t in tokens:
        token_ids.remove(t.token_id)
    for t in token_ids:
        new_token = PickToken(owner=token_owner, token_id=t)
        new_token.save()
        pixel_index = -1
        while True:
            pixel_index = randrange(0, MAX_PIXEL_INDEX)
            try:
                Pixel.objects.get(pixel_index=pixel_index)
            except Pixel.DoesNotExist:
                break

        new_pixel = Pixel(token_id=new_token.id, pixel_index=pixel_index, color="")
        new_pixel.save()
