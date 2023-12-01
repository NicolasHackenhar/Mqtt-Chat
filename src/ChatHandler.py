import json
import datetime
import os


class ChatHandler:

    def __init__(self, user) -> None:
        self.user = user
        self.pending_chats = {}
        self.active_chats = {}
        self.user_messages = {}

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
    
    def send_group_message(self, user, group, message):
        topic = f"GROUPS/{group}/messages"
        payload = json.dumps({
            "user": user, 
            "message": message, 
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        qos = 2
        retain = False

        return topic, payload, qos, retain
    
    def send_user_message(self, user, target, message):
        topic = self.active_chats.get(target).get('topic')
        payload = json.dumps({
            "user": user, 
            "message": message, 
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        qos = 2
        retain = False

        return topic, payload, qos, retain
    
    def handle_new_chat_request_message(self, message):
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
            self.active_chats[user]["messages"] = {}
    

    def handle_new_chat_message(self, message, topic):
        user = message['user']
        content = message['message']
        created_at = message['created_at']

        if topic not in self.user_messages:
            self.user_messages[topic] = []

        self.user_messages[topic].append({"usuario": user, "recebida_em": created_at, "mensagem": content})


    def print_chat_structure(self, target=None, topic=None):

        if topic is None and target is not None:
            topic = self.active_chats.get(target).get('topic')

        if target is None:
            topics_to_usernames = {chat_info['topic']: username for username, chat_info in self.active_chats.items()}
            target = topics_to_usernames.get(topic)

        os.system('clear')
        print("Conversando com " + target + ". Digite \sair pra sair da conversa.\n")

        if topic in self.user_messages:
            for message in self.user_messages[topic]:
             user = message['usuario']
             if  user == self.user:
                user = "Você"
             print(f"{user} ({message['recebida_em']}): {message['mensagem']}")
        print("\nVocê:")