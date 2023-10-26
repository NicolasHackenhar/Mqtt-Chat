import paho.mqtt.client as mqtt
import json

class LoginPublisher:
    def __init__(self, user):
        self.client = None
        self.user = user

    def login(self):
        if self.client != None:
            print(f"Usuário {self.user} já está logado.")
            return
    
        self.client = mqtt.Client(client_id=f"{self.user}_loginPublisher", clean_session=True)
        payload = json.dumps({"user": self.user, "status": "online"})
        self.client.connect(host="localhost")
        self.client.publish(
            topic=f"USERS/{self.user}", 
            payload=payload,
            qos=1, 
            retain=True)

        self.client.will_set(
            topic=f"USERS/{self.user}", 
            payload=f"{self.user} - offline",
            qos=1, 
            retain=True)
        
    def logout(self):
        payload = json.dumps({"user": self.user, "status": "offline"})
        self.client.publish(
        topic=f"USERS/{self.user}", 
        payload=payload,
        qos=1, 
        retain=True)
        self.client.disconnect()
        self.user = None
