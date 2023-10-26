import paho.mqtt.client as mqtt
import json
import datetime

class GroupPublisher:
    def __init__(self, user, groupName):
        self.client = mqtt.Client(client_id=f"{user}_{groupName}_publisher", clean_session=True)
        self.user = user
        self.groupName = groupName

    def create(self):
        payload = json.dumps({"user": self.user, "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        self.client.connect(host="localhost")
        self.client.publish(
            topic=f"GROUPS/{self.groupName}/owner", 
            payload=payload,
            qos=1, 
            retain=True)
        
    def add_member(self):
        payload = json.dumps({"user": self.user, "added_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        self.client.connect(host="localhost")
        self.client.publish(
            topic=f"GROUPS/{self.groupName}/members/{self.user}", 
            payload=payload,
            qos=1, 
            retain=True)