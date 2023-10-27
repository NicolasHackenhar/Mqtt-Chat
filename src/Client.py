import paho.mqtt.client as mqtt
import threading
import json
from src.StatusHandler import StatusHandler
from src.GroupHandler import GroupHandler
from src.ChatHandler import ChatHandler

class Client:
    def __init__(self, user):
        self.user = user
        self.statusHandler = StatusHandler()
        self.groupHandler = GroupHandler()
        self.chatHandler = ChatHandler()

        self.client = mqtt.Client(client_id=f"{self.user}", clean_session=False)
        self.client.connect(host="localhost")
        self.client.on_message = self.on_message
        thread_loop_start = threading.Thread(target=self.client.loop_start, daemon=True)
        self.login()
        thread_loop_start.start()
        self.client.subscribe("USERS/#")
        self.client.subscribe("GROUPS/#")
        self.client.subscribe(f"CONTROL/{self.user}_Control/chat_requests/#")
        self.client.subscribe(f"CONTROL/{self.user}_Control/active_chats/#")

    def on_message(self, client, userdata, message):
        # print(f"Received message '{message.payload.decode('utf-8')}' on topic '{message.topic}' with QoS {message.qos}")
        topic = message.topic.split("/")
        messagePayload = json.loads(message.payload.decode("utf-8"))

        if topic[0] == 'USERS':
            self.statusHandler.handle_status_message(message=messagePayload)
        elif topic[0] == 'GROUPS':
            if topic[2] == 'owner':
                self.groupHandler.handle_new_group_message(name=topic[1], message=messagePayload)
            elif topic[2] == "members":
                self.groupHandler.handle_new_member_message(name=topic[1], message=messagePayload, member=topic[3])
        elif topic[0] == 'CONTROL':
            if topic[2] == 'chat_requests':
                self.chatHandler.handle_new_chat_message(message=messagePayload)

    def login(self):
        topic, payload, qos, retain = self.statusHandler.login(self.user)
        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)

        topic, payload, qos, retain = self.statusHandler.logout(self.user)
        self.client.will_set(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)
    
    def logout(self):
        topic, payload, qos, retain = self.statusHandler.logout(self.user)
        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)

        self.client.disconnect()

    def create_group(self, name):
        topic, payload, qos, retain = self.groupHandler.create(self.user, name)
        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)

        topic, payload, qos, retain = self.groupHandler.add_member(self.user, name)
        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)

    def new_chat(self, user_target):
        topic, payload, qos, retain = self.chatHandler.new(self.user, user_target)
        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)

    def accept_chat(self, user_target):
        topic, payload, qos, retain = self.chatHandler.accept_self(self.user, user_target)
        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)
        
        topic, payload, qos, retain = self.chatHandler.accept_target(self.user, user_target)

        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)

        #TODO: implementar publicação no tópico do usuário que solicitou a conversa



    
        