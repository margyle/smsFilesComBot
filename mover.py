import time, requests, json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

headers = {'content-type': 'application/json',
'X-FilesAPI-Key': 'YOUR FILES.COM API KEY'
}

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

            
            strippedFile = event.src_path.replace('img/','')
            
            #make start upload call to files.com API(file upload is a three step process)
            urlBase1 = 'https://YOURSUBDIRECTORY.files.com/api/rest/v1/files/YOUR_DIRECTORY/' + strippedFile + '/?action=put'
            #debug
            print ('****url base=' + urlBase1)

            r = requests.post(urlBase1, headers=headers)
            jsonResponse = r.json()
            print(jsonResponse)
            #get vars for subsequent calls
            uploadUri = jsonResponse['upload_uri']
            uploadRef = jsonResponse['ref']

            #upload actual file
            data = open(event.src_path, 'rb').read()
            r2 = requests.put(url=uploadUri,
                    data=data,
                    headers={'Content-Type': 'application/octet-stream'})
            print(r2)

            #close out the upload!
            urlBase2 = 'https://YOURSUBDIRECTORY.files.com/api/rest/v1/files/YOUR_DIRECTORY/' + strippedFile + '/?action=end&ref=' + uploadRef
            #send the request
            r3 = requests.post(urlBase2, headers=headers)
            print(r3)



if __name__ == '__main__':
    w = Watcher()
    w.run()
