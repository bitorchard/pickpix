from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.db.models import IntegerField
from django.db.models.functions import Cast

import time
import traceback
import os
import pwd
import grp
import logging
import json
import requests
from random import randrange
from datetime import datetime, timedelta
from pathlib import Path
from typing_extensions import override

from openai import OpenAI
from openai import AssistantEventHandler
from django.core.cache import cache

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

API_KEY = 'NONE'
URL_BASE = 'https://api.openai.com/v1/%s'


def banner(msg):
   log.info(f"--------------- {msg} ---------------")


class Cache():
    """
    Simple cache
    """
    def __init__(self):
        self.d = {}

    def get(self, key):
        return self.d.get(key)

    def set(self, key, value):
        self.d['key'] = value


@csrf_exempt
def generate_content(request):
    """
    Generate response from ChatGPT Assistant using request keywords and sentiment
    """
    sentiment_str = "positive"
    if request.method == "POST":
        query_string = ""
        log.info(f"Request body: {request.body}")
        json_data = json.loads(request.body)
        sentiment = json_data.get('sentiment')
        if sentiment == 'negative_sentiment':
            sentiment_str = "negative"
        keywords = json_data.get('keywords')
        if keywords is not None:
            query_string = " and ".join([f"'{k}'" for k in keywords])
        log.info(f"GPT query string: {query_string}")
    thread = get_active_thread()
    file_ids = []
    thread_id = thread.id
    add_message_to_thread(thread_id, f"tell me your {sentiment_str} opinion of: \"{query_string}\"", file_ids)
    client = get_openai_client()
    assistant = create_assistant()
    banner("Execute Run")
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant['id']
    )
    banner("Wait For Run Completion")
    while run.status in ['queued', 'in_progress', 'cancelling']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
    banner(f"Run Completed With Status: '{run.status}'")
    if run.status == 'completed':
        banner(f"Fetch Messages")
        messages = client.beta.threads.messages.list(
            thread_id=thread_id
        )
        response = messages.data[0].content[0].text.value
    else:
        log.info(f"Reason for run failure: '{run.last_error}'")
        log.info(run.status)
    return JsonResponse({'message' : response})


def index(request):
    """
    Render the main page
    """
    template = loader.get_template('arsenal/arsenal.html')
    context = {}
    return HttpResponse(template.render(context, request))


def get_openai_client():
    """
    Instantiate Assistants client
    """
    client = cache.get("openai_client")
    if client:
        return client
    return OpenAI(api_key=API_KEY)


def get_threads():
    """
    Fetch list of requests threads
    """
    url = URL_BASE % f'threads'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'OpenAI-Beta' : 'assistants=v1'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        log.info("Thread data fetched successfully.")
        thread_data = response.json()
        log.info(thread_data)
        return thread_data['data']
    else:
        log.info(f"Failed to fetch thread data. Status code: {response.status_code}")
    return None


def get_files():
    """
    Fetch a list of uploaded files for augmented retrieval
    """
    url = URL_BASE % f'files'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'OpenAI-Beta' : 'assistants=v1'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        log.info("File data fetched successfully.")
        file_data = response.json()
        log.info(file_data)
        return file_data['data']
    else:
        log.info(f"Failed to fetch file data. Status code: {response.status_code}")
    return None


def add_message_to_thread(thread_id, message, file_ids):
    """
    Add query and lookup files to run thread 
    """
    url = URL_BASE % f'threads/{thread_id}/messages'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'OpenAI-Beta' : 'assistants=v1'
    }
    data = {
        'role' : 'user',
        'content' : message,
        'file_ids' : file_ids
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200 or response.status_code == 201:
        log.info("Thread message added successfully.")
        message_data = response.json()
        log.info(message_data)
        return message_data
    else:
        log.info(f"Failed to add message. Status code: {response.status_code} {response.content}")
    return None


def get_active_thread():
    """
    Fetch an active thread or create it if there is none
    """
    thread = cache.get("active_thread")
    if thread is None:
        thread = create_thread()
        thread_id = thread.id
    else:
        if hasattr(thread, 'id'):
            thread_id = thread.id
        else:
            thread_id = thread['id']
        thread = get_thread_by_id(thread_id)
        if thread is None:
            thread = create_thread()
            thread_id = thread.id
    log.info("Active thread: %s (%s)" % (thread, thread_id))
    return thread_id


def create_run(thread_id, assistant_id):
    """
    Create an execution run
    """
    client = get_openai_client()
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    return run


def create_thread():
    """
    Create an execution thread
    """
    client = get_openai_client()
    thread = client.beta.threads.create()
    log.info("Created thread: %s (%s)" % (thread, thread.id))
    return thread


def list_models():
    """
    List available OpenAI models
    """
    url = URL_BASE % f'models'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'OpenAI-Beta' : 'assistants=v1'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        log.info("Models fetched successfully.")
        models = response.json()
        log.info(models)
        return models['data']
    else:
        log.info(f"Failed to fetch models. Status code: {response.status_code}")
    return None


def create_assistant():
    """
    Create OpenAI assistant
    """
    name = 'Arsenal Bot'
    assistant = get_assistant_by_name(name)
    if assistant:
        return assistant
    desc = "You are an opinion generator about the EPL team Arsenal FC. Whatever you are asked, you will respond with opinions and only about Arsenal FC (or related content)."
    instr = """You are an opinion bot, generating tweets about the EPL team Arsenal FC. Whatever you are asked, you will respond with opinions and only about Arsenal FC (or related content).
1. Your response must be in one to two sentences.
2. It should in a casual, conversational style, but using minimal slang. Don't use complex words.
3. Try to include some commentary about whether Arsenal are heading in the right or wrong direction and who's responsible.
4. You should either be very positive or negative, no neutral responses.
5. You must constrain your responses to the certain keywords and topics the user asks for.
6. Your opinion should be on a scale of 1 to 5 from serious to absurd. The prompt will indicate your response level."""

    client = get_openai_client()
    thread = client.beta.threads.create()
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instr,
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-1106"
    )
    return assistant


def get_assistant_by_name(assistant_name):
    """
    Fetch OpenAI Assistant by name
    """
    assistants = get_assistants()
    if assistants is None:
        return None
    for a in assistants:
        if a['name'] == assistant_name:
            return a
    return None


def get_assistants():
    """
    Fetch a list of OpenAI Assistants for this account
    """
    url = URL_BASE % f'assistants'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'OpenAI-Beta' : 'assistants=v1'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        log.info("Assistants fetched successfully.")
        assistants = response.json()
        log.info(assistants)
        return assistants['data']
    else:
        log.info(f"Failed to fetch assistants. Status code: {response.status_code} {response.content}")
    return None


def get_thread_by_id(thread_id):
    """
    Fetch an execution thread by id
    """
    url = URL_BASE % f'threads/{thread_id}'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'OpenAI-Beta' : 'assistants=v1'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        log.info("Thread data fetched successfully.")
        thread_data = response.json()
        log.info(thread_data)
        return thread_data
    else:
        log.info(f"Failed to fetch thread data. Status code: {response.status_code}")
    return None
