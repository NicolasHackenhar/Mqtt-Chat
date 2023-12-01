import json
import datetime
import os


class GroupHandler:

    def __init__(self, user):
        self.groups = {}
        self.user = user

    def create(self, name):
        payload = json.dumps({"user": self.user, "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        topic = f"GROUPS/{name}/owner"
        qos = 0
        retain = True
        return topic, payload, qos, retain
    
    def add_member(self, member, name):
        payload = json.dumps({"user": member, "status": "Aprovado"})
        topic = f"GROUPS/{name}/members/{member}"
        qos = 0
        retain = True
        return topic, payload, qos, retain
    
    def request_group_membership(self, member, name):
        payload = json.dumps({"user": member, "status": "Pendente"})
        topic = f"GROUPS/{name}/members/{member}"
        qos = 0
        retain = True
        return topic, payload, qos, retain

            
    def handle_new_group_creation_message(self, name, message):
        self.groups[name] = {}
        self.groups[name]["lider"] = {}
        self.groups[name]["lider"] = message["user"]
        self.groups[name]["criacao"] = {}
        self.groups[name]["criacao"] = message["created_at"]
        self.groups[name]["membros"] = {}
        self.groups[name]["messages"] = []

    def handle_new_group_message(self, group, message):
        user = message['user']
        content = message['message']
        created_at = message['created_at']

        if group in self.groups:
            if self.user in self.groups.get(group).get("membros"):
                self.groups[group]["messages"].append({"usuario": user, "recebida_em": created_at, "mensagem": content})

    def handle_member_added_message(self, name, message, member):
        self.groups[name]["membros"][member] = {}
        self.groups[name]["membros"][member] = message["status"]

    def print_chat_structure(self, group):
        os.system('clear')
        print("Conversando no grupo " + group + ". Digite \sair pra sair da conversa.\n")

        for message in self.groups[group]["messages"]:
             user = message['usuario']
             if  user == self.user:
                user = "Você"
             print(f"{user} ({message['recebida_em']}): {message['mensagem']}")
        print("\nVocê:")
            