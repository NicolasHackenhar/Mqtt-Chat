import json
import datetime

class ChatHandler:

    def __init__(self) -> None:
        self.pending_chats = {}
        self.active_chats = {}

    def new(self, user, user_target):
        topic = f"CONTROL/{user_target}_Control/chat_requests/{user}"
        payload = json.dumps({
            "user": user, 
            "status": "Aguardando aprovação", 
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        qos = 0
        retain = True

        return topic, payload, qos, retain
    
    def accept_self(self, user, user_target):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        topic = f"CONTROL/{user}_Control/chat_requests/{user_target}"
        payload = json.dumps({
            "user": user_target, 
            "status": "Aprovado",
            "topic": f"{user}_{user_target}_{now}", 
            "started_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        qos = 0
        retain = True

        return topic, payload, qos, retain
    
    def accept_target(self, user, user_target):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        topic = f"CONTROL/{user_target}_Control/chat_requests/{user}"
        payload = json.dumps({
            "user": user, 
            "status": "Aprovado",
            "topic": f"{user}_{user_target}_{now}", 
            "started_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        qos = 0
        retain = True

        return topic, payload, qos, retain

    
    def handle_new_chat_message(self, message):
        user = message['user']
        status = message['status']

        if status == "Aguardando aprovação":
            self.pending_chats[user] = {}
            self.pending_chats[user]["status"] = {}
            self.pending_chats[user]["status"] = message['status']
            self.pending_chats[user]["criacao"] = {}
            self.pending_chats[user]["criacao"] = message['created_at']
        elif status == 'Aprovado':
            self.active_chats[user] = {}
            self.active_chats[user]["status"] = {}
            self.active_chats[user]["status"] = message['status']
            self.active_chats[user]["iniciado"] = {}
            self.active_chats[user]["iniciado"] = message['started_at']
            self.active_chats[user]["topic"] = {}
            self.active_chats[user]["topic"] = message['topic']
      