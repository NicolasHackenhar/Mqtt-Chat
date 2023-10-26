import paho.mqtt.client as mqtt
import json
import time


class GroupSubscriber:
    def __init__(self, user, mutexGroupSubscriber):
        # clean session True é não persistente
        self.client = mqtt.Client(f"{user}_groupSubscriber")
        self.mutexGroupSubscriber = mutexGroupSubscriber
        self.groups = {}

    def show_groups(self):
        self.client.connect("localhost")

        self.client.loop_start()
        self.client.subscribe("GROUPS/#")
        self.client.on_message = self.on_message
        time.sleep(30)
        self.client.loop_stop()
        self.client.disconnect()

    def on_message(self, client, userdata, message):
        with self.mutexGroupSubscriber:
            messagePayload = json.loads(message.payload.decode("utf-8"))
            topic = message.topic.split("/")
            groupName = topic[1]
            attribute = topic[2]
            if attribute == "owner":
                self.groups[groupName] = {}
                self.groups[groupName]["lider"] = {}
                self.groups[groupName]["lider"] = messagePayload["user"]
                self.groups[groupName]["criacao"] = {}
                self.groups[groupName]["criacao"] = messagePayload["created_at"]
                self.groups[groupName]["membros"] = {}
            elif attribute == "members":
                memberUser = topic[3]
                self.groups[groupName]["membros"][memberUser] = {}
                self.groups[groupName]["membros"][memberUser] = messagePayload["added_at"]
