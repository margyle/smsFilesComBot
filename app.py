import requests
from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse

#dir to save the inbound images
DOWNLOAD_DIRECTORY = 'img'
app = Flask(__name__)

#webook debug
@app.route("/newFile", methods=['GET', 'POST'])
def hello_world():
    print("webhook working!")
    return {"success": "true"}, 200

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    resp = MessagingResponse()
    if request.values['NumMedia'] != '0':
        # Use the message SID as a filename.
        filename = request.values['MessageSid'] + '.png' 
        with open('{}/{}'.format(DOWNLOAD_DIRECTORY, filename), 'wb') as f:
           image_url = request.values['MediaUrl0']
           f.write(requests.get(image_url).content)
           print("New Inbound Image")
        print("Completed")
        
        resp.message("Thanks for the image!")
    else:
        resp.message("Thats not a picture!")
        
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
