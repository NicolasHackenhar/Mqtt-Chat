import paho.mqtt.client as mqtt
import json
import datetime


class ChatPublisher:

    def __init__(self, user):
        self.user = user
        self.client = mqtt.Client(client_id=f"{self.user}_chatPublisher", clean_session=False)

    def newCoversation(self, userTarget): 
        payload = json.dumps({"user": self.user, "status": "Aguardando aprovação", "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        self.client.connect(host="localhost")
        self.client.publish(
            topic=f"CONTROL/{userTarget}_Control/chatRequests/{self.user}", 
            payload=payload,
            qos=1, 
            retain=True)
        
    def acceptConversation(self, userTarget):
        payload = json.dumps({"user": userTarget, "status": "Aprovado", "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        self.client.connect(host="localhost")
        self.client.publish(
            topic=f"CONTROL/{self.user}_Control/chatRequests/{userTarget}", 
            payload=payload,
            qos=1, 
            retain=True)
        self.client.publish(
            topic=f"CONTROL/{userTarget}_Control/chatRequests/{self.user}", 
            payload=payload,
            qos=1, 
            retain=True)
    
        
