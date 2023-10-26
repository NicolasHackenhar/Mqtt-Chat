import paho.mqtt.client as mqtt
import json
import time


class UsersSubscriber:
    def __init__(self, user, mutexUserStatus):
        self.client = mqtt.Client(
            f"{user}_usersSubscriber", clean_session=True)
        self.userStatus = {}
        self.mutexUserStatus = mutexUserStatus

    def show_users(self):
        self.client.connect("localhost")

        self.client.loop_start()
        self.client.on_message = self.on_message
        self.client.subscribe("USERS/#")
        time.sleep(30)
        self.client.loop_stop()
        self.client.disconnect()

    def on_message(self, client, userdata, message):
        with self.mutexUserStatus:
            messagePayload = json.loads(message.payload.decode("utf-8"))
            self.userStatus[messagePayload["user"]] = messagePayload["status"]
