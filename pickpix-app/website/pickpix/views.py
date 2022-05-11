from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import logging
import json
from .models import *
from random import randrange

log = logging.getLogger(__name__)

MAX_PIXEL_INDEX = 2500

def index(request):
    template = loader.get_template('pickpix/avax.html')
    pixel_ids = [p.pixel_index for p in Pixel.objects.all()]
    json_pixel_ids = json.dumps(pixel_ids)
    context = {'used_pixels' : json_pixel_ids}
    return HttpResponse(template.render(context, request))

@csrf_exempt
def token(request):
    if request.method == "POST":
        req_data = json.loads(request.body)

    log.info("Got token POST with '%s'" % req_data)
    insert_new_token(req_data)
    return HttpResponse(True)

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
