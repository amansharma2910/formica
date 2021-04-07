# Functions that interact with the backend go here

import discord
import os
import json
import requests
import globals

PARAMS = {}
# API endpoints
Q_URL = "" # questions
R_URL = "" # responses

    # API key

# keep performing get requests to get the most up to date data (querying mechanisms)



# Description: Gets the form details (eg. form name)
def get_form_specs():
    # get channel to send alerts to
    alert_channel_id = 824348394411262013
    # get form name
    form_name = "Event Registration"
    #form_alert_channel = client.get_channel(alert_channel_id)

    return alert_channel_id, form_name

# Description: Gets the questions and responses from the database
def get_form():
    # get questions (tmp; for local testing)
    with open("dummy_questions.json", "r") as q:
        globals.questions = json.load(q)
        q_count = len(globals.questions)

    # # get questions from database
    # get_questions = requests.get(url = Q_URL, params = PARAMS)
    # globals.questions = get_questions.json()

    # get responses (tmp; for local testing)
    with open('dummy_responses.json', 'r') as r:
        globals.local_responses = json.load(r)

    # # get responses from database
    # get_responses = requests.get(url = R_URL, params = PARAMS)
    # db_responses = []

    # # fill a local array with the database responses
    # globals.local_responses = []

    # for item in db_responses:
    #     responses = list(item["Response"].values()) # grab the responses
    #     globals.local_responses.append({'form_id': item['form_id'], 'username': "", 'user_id': item['user_id'], 'responses': responses, 'response_ids': []})
    
    return q_count

# Description: Writes the responses to the database, creates a submission confirmation message for the user and form creator
def submit_responses(user):
    globals.form_started = False

    # write to the database (tmp; for local testing)
    with open('dummy_responses.json', 'w') as w:
        json.dump(globals.local_responses, w)

    # # format responses to send to database
    # tmp_qs = []
    # db_responses = {}

    # for item in globals.questions:
    #     tmp_qs.append(item['question'])

    # for item in globals.local_responses:
    #     tmp_responses = {key:value for key, value in zip(tmp_qs, item['responses'])}
    #     db_responses.append({"form_id": item['form_id'], "user_id": item['user_id'], "Response": tmp_responses})
    
    # # send post request and save response
    # post_request = requests.post(url = R_URL, data = db_responses)
    
    
    #make submission confirmation for the user
    submission_alert_user = discord.Embed(title = 'Form submitted', description = 'You can view and manage your responses here: <insert link>', color = globals.form_color)

    # make a submission confirmation for the form creator
    submission_alert_creator = discord.Embed(title = f'{user} has submitted a form', description = 'To manage your forms, click here: <insert link>', color = globals.form_color)
    submission_alert_creator.add_field(name = 'Form:', value = globals.form_name, inline = False)

    return submission_alert_user, submission_alert_creator