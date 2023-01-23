import json

from channels.generic.websocket import WebsocketConsumer
from time import sleep


class TwitterConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(1,10):
            self.send(text_data=json.dumps(["werty","1111111","111111",i]))
            sleep(1)

    def disconnect(self, close_code):
        pass

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json["message"]

    #     self.send(text_data=json.dumps({"message": message}))