import paho.mqtt.client as mqtt
import json
import time


class ChatSubscriber:
    def __init__(self, user):
        # clean session True é não persistente
        self.client = mqtt.Client(
            f"{user}_chatSubscriber", clean_session=False)
        self.user = user
        #TODO: implementar mutex
        self.chats = {}

    def show_chat_requests(self):
        self.client.connect("localhost")

        self.client.loop_start()
        self.client.subscribe(f"CONTROL/{self.user}_Control/chatRequests/#")
        self.client.on_message = self.on_message
        time.sleep(30)
        self.client.loop_stop()
        self.client.disconnect()

    def on_message(self, client, userdata, message):
        messagePayload = json.loads(message.payload.decode("utf-8"))
        topic = message.topic.split("/")
        if topic[2] == "chatRequests":
            user = messagePayload['user']
            self.chats[user] = {}
            self.chats[user]["status"] = {}
            self.chats[user]["status"] = messagePayload['status']
            self.chats[user]["criacao"] = {}
            self.chats[user]["criacao"] = messagePayload['created_at']
