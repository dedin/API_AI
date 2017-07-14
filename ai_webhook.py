from flask import Flask, render_template
from flask import request, jsonify, json, make_response
from random import randint




app = Flask(__name__)

SAFE_MESSAGE = ["All is well.", "I am fine now", "Everything is alright"]
UNSAFE_MESSAGE = ["I am in trouble.", "I am scared", "I am currently not in a safe situation"]
VALID_ENTITIES = ["safe", "unsafe", "worried"]


@app.route('/', methods=['GET'])
def home():
    return render_template('speech.html')

@app.route('/webhook', methods=['POST'])
def home():
    #message = send_msgs
    #return message

    ai_request = request.get_json()
    print json.dumps(ai_request, indent=4)

    if ai_request.get("result").get("action") != "send.msg":
        print "ERROR MESSAGE IN ACTION"                                   #Service returns error code?
    situation_category = get_category(ai_request)
    if situation_category is None:
       pass                                                        # invalid situation category

    message = get_send_msg(situation_category)  # eventually the returned message will just be a success status/feedback
    print "\n\nMESSAGE IS {}\n\n\n".format(message)
    result = make_web_hook_result(message)
    web_hook_result = make_response(json.dumps(result))
    web_hook_result.headers['Content-Type'] = 'application/json'
    return web_hook_result


def make_web_hook_result(message):
    result = {"speech" : message,
              "displayText" : message,
              "data" : "",
              "contextOut" : "",
              "source" : ""}

    return result


def get_category(ai_request):
    situation_category = ai_request.get("result").get("parameters").get("situation-category")   # or a default value?
    if situation_category in VALID_ENTITIES:
        return situation_category
    else:
        print "INVALID CATEGORY OR ENTITY"
        return None


"""
    Function to send the message to responders
        - Get responders and their contacts
        - Get the message to send
        - Send the message.
        - Send success feedback to caller

    Questions:
    # - will we ever get a bad situation-category value from API.AI 
"""
def get_send_msg(situation_category):
    message = get_msg(situation_category)
    return message


"""
    Function to figure out the appropriate message to send to responders
    - Based on the given situation_category, figure out the appropriate message to send.
    - Return a string that is the message
    
    Questions: 
        Will a "safe" msg only be sent after a distress alert? Can it be sent at any other time? If so, does the content need to change?
"""


def get_msg(situation_category):
    random_number = randint(0,2)
    message = ""       # Or a default message just in case something goes wrong with all the checks
    if situation_category == "safe":
        message = SAFE_MESSAGE[random_number]
    elif situation_category == "unsafe":
        message = UNSAFE_MESSAGE[random_number]
    elif situation_category == "worried":
        pass
    return message


if __name__ == '__main__':
    #app.run(ssl_context = 'adhoc')
    app.run()