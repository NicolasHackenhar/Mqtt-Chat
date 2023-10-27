import json

class StatusHandler:
    def __init__(self):
        self.userStatus = {}

    def login(self, user):
        payload = json.dumps({"user": user, "status": "online"})
        topic = f"USERS/{user}"
        qos = 0
        retain = True
        return topic, payload, qos, retain
    
    def logout(self, user):
        payload = json.dumps({"user": user, "status": "offline"})
        topic = f"USERS/{user}"
        qos = 0
        retain = True
        return topic, payload, qos, retain
    
    def handle_status_message(self, message):
        self.userStatus[message["user"]] = message["status"]
