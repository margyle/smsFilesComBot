import time, requests, json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher:
    DIRECTORY_TO_WATCH = "img"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print("Received created event - %s." % event.src_path)

        elif event.event_type == 'modified':
            print ("Received modified event - %s." % event.src_path)

            filePath = event.src_path
            strippedFile = event.src_path.replace('img/','')
            #call the files.com API upload function
            files_api_upload(strippedFile,filePath)
            

def files_api_upload(strippedFile, filePath):
            headers = {'content-type': 'application/json',
            'X-FilesAPI-Key': '**YOUR API KEY***'
            }
            urlBase = 'https://**YOUR_SUBDOMAIN**.files.com/api/rest/v1/files/**YOUR FOLDER NAME**/'

            #make start upload call to files.com API
            startUploadUrl = urlBase + strippedFile + '/?action=put'

            r = requests.post(startUploadUrl, headers=headers)
            jsonResponse = r.json()
            print(jsonResponse)

            uploadUri = jsonResponse['upload_uri']
            uploadRef = jsonResponse['ref']

            #upload actual file
            data = open(filePath, 'rb').read()
            r2 = requests.put(url=uploadUri,
                    data=data,
                    headers={'Content-Type': 'application/octet-stream'})
            print(r2)

            #close out the upload!
            endUploadUri = urlBase + strippedFile + '/?action=end&ref=' + uploadRef
            #send the request
            r3 = requests.post(endUploadUir, headers=headers)
            print(r3)

if __name__ == '__main__':
    w = Watcher()
    w.run()
