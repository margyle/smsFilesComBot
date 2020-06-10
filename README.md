# smsFilesComBot
A quick and dirty flask app and directory monitor to send images to a Files.com server via inbound SMS messages 


# app.py
Complete Flask App that recieves SMS messages over the Twilio API and then uploads the images to your Files.com account via their REST API.

# mover.py
Directory monitor that uploads any newly saved files to your Files.com account via their REST API. If you just want to watch a folder and not expose to FLaks, use this script.
