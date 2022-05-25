from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.db.models import IntegerField
from django.db.models.functions import Cast

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

log = logging.getLogger(__name__)

CHAIN_ID = 43113
MIN_PRICE = 0.1*10**18
MAX_PIXEL_INDEX = 2500
PROVIDER_URL = 'https://api.avax-test.network/ext/bc/C/rpc'
CONTRACT_JSON_FILE = 'pickpix/contract.json'
CACHED_VOUCHER_KEY = 'CACHED_VOUCHER'
CACHED_VOUCHER_EXPIRATION_SECS = 30*60
PRIVATE_KEY = "e607298786fc31a8606539101856730258f0192f757664ca7198902e1d3ac713"

class Voucher:
    def __init__(self, uri, signature):
        self.uri = uri
        self.min_price = MIN_PRICE
        self.signature = signature
        self.creation_date = datetime.now()

    def to_signed_json():
        return {
            'minPrice' : MIN_PRICE,
            'uri' : self.uri,
            'signature' : self.signature,
        }

def index(request):
    template = loader.get_template('pickpix/avax.html')
    pixel_ids = [p.pixel_index for p in Pixel.objects.all()]
    json_pixel_ids = json.dumps(pixel_ids)
    context = {'used_pixels' : json_pixel_ids}
    render_secret_image()
    return HttpResponse(template.render(context, request))

@csrf_exempt
def token(request):
    if request.method == "POST":
        req_data = json.loads(request.body)

    log.info("Got token POST with '%s'" % req_data)
    check_latest_token()
    return HttpResponse(True)

def random_free_pixel():
    return 1

def voucher(request):
    voucher = request.session.get(CACHED_VOUCHER_KEY)
    if voucher:
        if not voucher.creation_date + time_delta(seconds=CACHED_VOUCHER_EXPIRATION_SECS) < datetime.now():
            return voucher

        del request.session[CACHED_VOUCHER_KEY]

    ipns_uri = generate_ipns()
    signature = generate_signature(MIN_PRICE, ipns_uri)
    voucher = Voucher(generate_ipns(), signature)
    request.session[CACHED_VOUCHER_KEY] = voucher

    return JsonResponse(voucher.to_signed_json())

def generate_signature(ipns_uri, min_price):
    w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

    with open(CONTRACT_JSON_FILE) as f:
        contract_json = json.load(f)

    data = {
        "types" : {
            "EIP712Domain": [
                { "name": "name", "type": "string" },
                { "name": "version", "type": "string" },
                { "name": "chainId", "type": "uint256" },
                { "name": "verifyingContract", "type": "address" },
            ],
            "NFTVoucher" : [
                { "name": "minPrice", "type": "uint256" },
                { "name": "uri", "type": "string" },
            ],
        },
        "domain" : {
            "chainId": CHAIN_ID,
            "name": "Pixel-Voucher",
            "verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
            "version": "1",
        },
        "primaryType": "NFTVoucher",
        "message" : {
            "minPrice" : min_price,
            "uri" : ipns_uri,
        }
    }

    signable = encode_structured_data(data)
    signed = w3.eth.account.sign_message(signable, PRIVATE_KEY)

    return signed.signature.hex()

def generate_ipns():
    return "ipns:///TEST_IPNS"

def check_latest_token():
    w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

    with open(CONTRACT_JSON_FILE) as f:
        contract_json = json.load(f)

    csum_address = Web3.toChecksumAddress(contract_json['address'])
    contract = w3.eth.contract(abi=contract_json['abi'], address=csum_address);

    last_token = contract.functions.lastToken().call()
    all_tokens = PickToken.objects.all()
    #db_token_max = int(all_tokens.aggregate(Max('token_id'))['token_id__max'])
    #db_token_max = PickToken.objects.all().annotate(int_token=Cast('token_id', IntegerField())).order_by('-int_token')[:1][0].int_token

    db_tokens = PickToken.objects.all().annotate(int_token=Cast('token_id', IntegerField())).order_by('-int_token')
    if db_tokens:
        db_token_max = db_tokens[:1][0].int_token
    else:
        db_token_max = 0

    log.info("max token: %s" % (db_token_max+1))
    log.info("last token: %s" % (last_token+1))
    if db_token_max != last_token:
        render_secret_image()

    for t in range(db_token_max+1, last_token+1):
        new_token = PickToken(owner="0x0", token_id=t)
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

def render_secret_image():
    ice_cream = Image.open("pickpix/ice_cream.jpg")
    ice_cream = ice_cream.convert('RGBA')

    MAX_ROW = 50
    MAX_COL = 50

    grid_size = ice_cream.size[0] / MAX_COL

    used_pixels = [p.pixel_index for p in Pixel.objects.all()]

    overlay = Image.new('L', (ice_cream.size[0], ice_cream.size[1]), 255)
    draw = ImageDraw.Draw(overlay)

    for p in used_pixels:
        x_coord = (p % MAX_COL) * grid_size
        y_coord = int(p / MAX_COL) * grid_size
        draw.rectangle((x_coord, y_coord, x_coord+grid_size, y_coord+grid_size), fill=0)

    ice_cream.paste(overlay, mask=overlay)
    ice_cream = ice_cream.convert('RGB')
    ice_cream.save('static/pickpix/secret_img.jpg')

    uid = pwd.getpwnam('www-data')[2]
    gid = grp.getgrnam('www-data')[2]
    os.chown('static/pickpix/secret_img.jpg', uid, gid)

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
