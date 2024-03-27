import json
from flask import Blueprint, jsonify, request
import os
import panel as pn
import openai
from dotenv import load_dotenv

load_dotenv()

pn.extension()
openai.api_key = os.getenv("OPENAI_API_KEY")
panels = []

F_messages = [{"role": "system", "content": """You are ChatBot, an automated Serviced to collect informations for an enterprise
You first greet the customer, then collect the service he wish to do,\ and then ask the detail information relative to that service. \
 You will present all the information the user is to enter and then progessively ask him those information one after the other 
  (eg if he is to enter the fuulname, email, contact, etc you first ask him his fullname, after submiting his full name you then ask the others) \
 You wait to collect the entire informations, then summerise it and check for a final confirmation \
 and the summarised information shouild not be numerated nor have hiphen \
 time if the customer want to add anything else. \
 Each time you present the summary always use the phrase (Here is a summary of the details) \
 And when presenting the summary details the attribut name should be seperated with _ not space (e.g Supplier Name: FLYT should be Supplier_Name: FLYT \
 Finally you collect the payment .\
 Make sure you clearify all options, extras and size to uniquely identify the iterm from the menu .\
 You respond in a short very conversional friendly style .\
 The service includes \
 Register Employee \
 Register Supplier \ """}]

inp = pn.widgets.TextInput(value='Hi', placeholder='Enter your message')

# title = pn.widgets.StaticText(value='MEFA ChatBot')
button_conversation = pn.widgets.Button(name='Submit')

chat_bp = Blueprint('chat', __name__)
def get_completion_from_messages(messages):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content

@chat_bp.post('/chat')
def end_point():
    data = request.get_json()
    F_messages.append({'role': 'user', 'content': f"{data.get('message')}"})
    response = get_completion_from_messages(F_messages)
    F_messages.append({'role': 'assistant', 'content': f"{response}"})
    if "Here is a summary of the details" in response:
        summary_text = response.split("Here is a summary of the details:")[1].strip()
        print(summary_text)
        response = convertToJson(summary_text)
        print(response.get('Addresse'))
        return response
    return jsonify({'message': f"{response}"}) , 201
# def collect_messages(_):
#     prompt = inp.value_input
#     inp.value=''
#     F_messages.append({'role':'user', 'content':f"{prompt}"})
#     response = get_completion_from_messages(F_messages)
#     F_messages.append({'role':'assistant', 'content':f"{response}"})
#     user_row = pn.Row('<b>User:</b>', pn.pane.Markdown(prompt, width=600))
#     assistant_row = pn.Row('<b>Assistant:</b>', pn.pane.Markdown(response, width=600))
#     user_row[0].css_classes.append('user-label')
#     assistant_row[0].css_classes.append('assistant-label')
#     panels.extend([user_row, assistant_row])
#     if "Here is a summary of the details" in response:
#         summary_text = response.split("Here is a summary of the details:")[1].strip()
#         print(summary_text)
#         convertToJson(summary_text)
#         details = summary_text.split("Do you confirm these details?")[0].strip()  # Split by double newline to get details
#         print("Summary:")
#         print(details)
#         print("\n")
#
#     return pn.Column(*panels)
#
# # dict([entry.split('Supplier_')[1].split(":") for entry in text.split("\n")])
def convertToJson(summary_text):
    summary_dict = {}
    for line in summary_text.strip().split("\n"):
        parts = line.split(": ", 1)
        if len(parts) == 2:
            key, value = parts
            summary_dict[key.strip()] = value.strip()

    # Convert the dictionary to JSON
    summary_json = json.dumps(summary_dict, indent=4)
    print(summary_json)
    return summary_json;
#
# interactive_conversation = pn.bind(collect_messages, button_conversation)
#
# custom_style = {
#         "border": "1px solid #ccc",
#         "padding": "10px",
#         "overflow": "auto",
#         "max-height": "500px",  # Adjust as needed
# }
# output_panel = pn.panel(interactive_conversation,styles=custom_style, loading_indicator=True)
#
# pn.config.raw_css.append('.user-label { color: blue; }')
# pn.config.raw_css.append('.assistant-label { color: red; }')
#
# title = pn.widgets.StaticText(value='<h1>MEFA ChatBot</h1>', align='center')
#
# dashboard = pn.Column(
#     title,
#     output_panel,
#     pn.Row( inp, button_conversation)
#
# )
#
# dashboard.servable()
# pn.serve(dashboard)