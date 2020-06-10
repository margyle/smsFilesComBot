import requests, time, json
from flask import Flask, request, redirect, jsonify
from twilio.twiml.messaging_response import MessagingResponse

#dir to save the inbound images
DOWNLOAD_DIRECTORY = 'img'
app = Flask(__name__)

#files.com webook debug
@app.route("/newFile", methods=['GET', 'POST'])
def hello_world():
    print("Webhook working!")
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
        
        #call the files.com API upload function
        files_api_upload(filename)
        
        print("Completed")

        resp.message("Thanks for the image!")
    else:
        resp.message("Thats not a picture!")

    return str(resp)

def files_api_upload(filename):
            #time.sleep(5)
            headers = {'content-type': 'application/json',
            'X-FilesAPI-Key': '**YOUR API KEY***'
            }
            urlBase = 'https://**YOUR_SUBDOMAIN**.files.com/api/rest/v1/files/**YOUR FOLDER NAME**/'

            #make start upload call to files.com API
            startUploadUrl = urlBase + filename + '/?action=put'

            r = requests.post(startUploadUrl, headers=headers)
            jsonResponse = r.json()
            print(jsonResponse)
            
            #get params for next call
            uploadUri = jsonResponse['upload_uri']
            uploadRef = jsonResponse['ref']

            #upload actual file
            data = open('img/' + filename, 'rb').read()
            r2 = requests.put(url=uploadUri,
                    data=data,
                    headers={'Content-Type': 'application/octet-stream'})
            print(r2)

            #close out the upload!
            endUploadURl = urlBase + filename + '/?action=end&ref=' + uploadRef
            #send the request
            r3 = requests.post(endUploadURl, headers=headers)
            print(r3)
            print("File uploaded!")


if __name__ == "__main__":
    app.run(debug=True)
