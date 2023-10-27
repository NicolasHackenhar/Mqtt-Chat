import json
import datetime


class GroupHandler:

    def __init__(self):
        self.groups = {}

    def create(self, user, name):
        payload = json.dumps({"user": user, "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        topic = f"GROUPS/{name}/owner"
        qos = 0
        retain = True
        return topic, payload, qos, retain
    
    def add_member(self, member, name):
        payload = json.dumps({"user": member, "added_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        topic = f"GROUPS/{name}/members/{member}"
        qos = 0
        retain = True
        return topic, payload, qos, retain
            
    def handle_new_group_message(self, name, message):
        self.groups[name] = {}
        self.groups[name]["lider"] = {}
        self.groups[name]["lider"] = message["user"]
        self.groups[name]["criacao"] = {}
        self.groups[name]["criacao"] = message["created_at"]
        self.groups[name]["membros"] = {}

    def handle_new_member_message(self, name, message, member):
        self.groups[name]["membros"][member] = {}
        self.groups[name]["membros"][member] = message["added_at"]