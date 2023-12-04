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
        self.groupHandler = GroupHandler(self.user)
        self.chatHandler = ChatHandler(self.user)

        self.inChat = False
        self.session = None

        self.client = mqtt.Client(client_id=f"{self.user}",  protocol=mqtt.MQTTv5, reconnect_on_failure=False)
        self.client.connect(host="localhost", clean_start=False)
        self.client.on_message = self.on_message
        self.client.on_connect = self.connect_callback
        self.client.on_disconnect = self.disconnect_callback
        # self.client.on_log = self.log_callback
        thread_loop_start = threading.Thread(target=self.client.loop_start, daemon=True)
        self.login()
        thread_loop_start.start()
        self.client.subscribe("USERS/#", 2)
        self.client.subscribe("GROUPS/#", 2)
        self.client.subscribe(f"CONTROL/{self.user}_Control/chat_requests/#", 2)
        self.client.subscribe(f"CONTROL/{self.user}_Control/active_chats/#", 2)


    def log_callback(self, client, userdata, level, string):
        print(f"Log: {string}")

    def connect_callback(self, client, userdata, flags, reasonCode, properties):
        print(f"Connection: {reasonCode}")

    def disconnect_callback(self, client, userdata, reasonCode, properties):
        print(f"Connection lost with reason code: {reasonCode}")
        exit()

    def subscribeActiveChats(self):
        for user, attributes in self.chatHandler.active_chats.items():
            self.client.subscribe(topic=attributes['topic'], options=mqtt.SubscribeOptions(qos=2, noLocal=False))

    def on_message(self, client, userdata, message):
        # print(f"Received message '{message.payload.decode('utf-8')}' on topic '{message.topic}' with QoS {message.qos}")
        topic = message.topic.split("/")
        messagePayload = json.loads(message.payload.decode("utf-8"))

        if any(topic[0] == valor['topic'] for _, valor in self.chatHandler.active_chats.items()):
            self.chatHandler.handle_new_chat_message(message=messagePayload, topic=topic[0])
            if self.inChat == True and self.session == topic[0]:
                self.chatHandler.print_chat_structure(topic=topic[0])

             
        if topic[0] == 'USERS':
            self.statusHandler.handle_status_message(message=messagePayload)
        elif topic[0] == 'GROUPS':
            if topic[2] == 'owner':
                self.groupHandler.handle_new_group_creation_message(name=topic[1], message=messagePayload)
            elif topic[2] == "members":
                self.groupHandler.handle_member_added_message(name=topic[1], message=messagePayload, member=topic[3])
            if topic[2] == "messages":
                self.groupHandler.handle_new_group_message(group=topic[1], message=messagePayload)
                if self.inChat == True and self.session == topic[1]:
                    self.groupHandler.print_chat_structure(group=topic[1])
        
        elif topic[0] == 'CONTROL':
            if topic[2] == 'chat_requests':
                self.chatHandler.handle_new_chat_request_message(message=messagePayload)
                if messagePayload['status'] == 'Aprovado':
                    self.client.subscribe(topic=messagePayload['topic'], options=mqtt.SubscribeOptions(qos=2, noLocal=False))
            if topic[2] == 'active_chats':
                self.chatHandler.handle_new_chat_message(message=messagePayload, topic=topic[3])

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

    def create_group(self, name):
        topic, payload, qos, retain = self.groupHandler.create(name)
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
        
    def add_member(self, user, group):
        topic, payload, qos, retain = self.groupHandler.add_member(user, group)
        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)

        
    def request_group_membership(self, name):
        topic, payload, qos, retain = self.groupHandler.request_group_membership(self.user, name)
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
        #TODO: está enviando solicitação de aceite pra usuário que não tem solicitação pendente

        topic, payload, qos, retain = self.chatHandler.accept_target(self.user, user_target)

        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)
        
        message = json.loads(payload)

        self.client.subscribe(topic=message['topic'], options=mqtt.SubscribeOptions(qos=2, noLocal=False))

        del self.chatHandler.pending_chats[user_target]


    def send_group_message(self, group,  message):
        #TODO: validar se o usuário está no grupo
        topic, payload, qos, retain = self.groupHandler.send_group_message(self.user, group, message)
        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)

    def send_user_message(self, target, message):
        #TODO: validar se o usuários possuem um chat ativo
        topic, payload, qos, retain = self.chatHandler.send_user_message(self.user,target, message)
        self.client.publish(
            topic=topic, 
            payload=payload,
            qos=qos, 
            retain=retain)
        