import threading
import os
import time
from src.Client import Client

mutexTerminal = threading.Lock()

def imprimirMenu():
	with mutexTerminal:
		print("Bem vindo ao chat")
		print(f"Você está logado como: {client.user}")
		print("1. Visualizar usuários")
		print("2. Criar grupo")
		print("3. Visualizar grupos")
		print("4. Entrar em grupo")
		print("5. Iniciar conversa")
		print("6. Visualizar solicitações de conversa")
		print("7. Aceitar solicitação de conversa")
		print("8. Enviar mensagem")
		print("9. Gerenciar grupo")
		print("10. Sair")
	
		print("")

def visualizar_usuarios():
	with mutexTerminal:
		os.system('clear')
		print_users()
		print()
		input("Pressione enter para voltar ao menu.")

def print_users():
	for user, status in client.statusHandler.userStatus.items():
				print(f"Usuário {user} está {status}")

def criar_grupo():
	with mutexTerminal:
		os.system('clear')
		name = input("Digite o nome do grupo ou \\voltar para voltar ao menu: ")
		if name == "\\voltar":
			return
		name = name.strip()
		if name != "":
			client.create_group(name=name)
			print("Grupo criado com sucesso")
			input("Pressione enter para voltar ao menu.")

def visualizar_grupos():
	with mutexTerminal:
		print_groups()
		input("Pressione enter para voltar ao menu.")

def print_groups():
	os.system('clear')
	for group, attribute in client.groupHandler.groups.items():
		print(f"Grupo {group}: ")
		for key, value in attribute.items():

			if key == "messages":
				continue

			if key == "membros":
				print(f"\t{key}:")
				for memberName, status in value.items():
					if status == 'Aprovado':
						print(f"\t\t{memberName}")
			else:
				print(f"\t{key}: {value}")
		print("")

def entrar_grupo():
	with mutexTerminal:
		print_groups()
		group = input("Digite o nome do grupo ou \\voltar para voltar ao menu: ")
		if group == "\\voltar":
			return
		group = group.strip()
		if group != "":
			client.request_group_membership(name=group)
			print("Solicitação enviada ao líder do grupo")
			input("Pressione enter para voltar ao menu.")



def iniciar_conversa():
	with mutexTerminal:
		#TODO: validar se já existe um chat ativo entre os usuários
		os.system('clear')
		print_users()
		user_target = input("\nInforme o usuário com quem deseja se comunicar ou \\voltar para voltar ao menu:")
		if user_target == "\\voltar":
			return
		user_target = user_target.strip()
		if user_target != "":
			client.new_chat(user_target=user_target)
			print("Solicitação enviada com sucesso")
			input("Pressione enter para voltar ao menu.")

def visualizar_solicitacoes_conversa():
	with mutexTerminal:
		os.system('clear')
		print_pendind_chats()	
		print_active_chats()
		input("Pressione enter para voltar ao menu.")

def print_pendind_chats():
	for user, attributes in client.chatHandler.pending_chats.items():
		print(f"Usuário: {user}")
		print(f"\tStatus: {attributes['status']}")
		print(f"\tSolicitado em: {attributes['criacao']}")

def print_active_chats():
	for user, attributes in client.chatHandler.active_chats.items():
		print(f"Usuário: {user}")
		print(f"\tStatus: {attributes['status']}")
		print(f"\tIniciado em: {attributes['iniciado']}")
		print(f"\tTópico: {attributes['topic']}")

def aceitar_solicitacao_conversa():
	with mutexTerminal:
		#TODO: validar se já existe um chat ativo entre os usuários
		os.system('clear')
		print_pendind_chats()
		user_target = input("Informe o usuário com quem deseja se comunicar ou \\voltar para voltar ao menu:")
		if user_target == "\\voltar":
			return
		user_target = user_target.strip()
		if user_target != "":
			client.accept_chat(user_target=user_target)
			print("Solicitação aprovada com sucesso")
			input("Pressione enter para voltar ao menu.")

def enviar_mensagem():
	with mutexTerminal:
		os.system('clear')
		target_type = input("Selecione o destino da mensagem: (1) Grupo (2) Usuário: ")
		os.system('clear')
		if target_type == "1":
			print_active_groups()
			group = input("Informe o nome do grupo: ")
			os.system('clear')
			send_group_message(group)

		elif target_type == "2":
			print_active_chats()
			target = input("Informe o nome do usuário: ")
			os.system('clear')
			send_message(target=target)

def send_group_message(group):
	client.inChat = True
	client.session = group
	client.groupHandler.print_chat_structure(group=group)
	while True:
		message = input("")
		message = message.strip()
		if message == "\\sair":
			client.inChat = False
			client.session = None
			return
		if message != "":
			client.send_group_message(group=group, message=message)

def send_message(target):
	client.inChat = True
	client.session = client.chatHandler.active_chats.get(target).get('topic')
	client.chatHandler.print_chat_structure(target=target)
	while True:
		message = input("")
		message = message.strip()
		if message == "\\sair":
			client.inChat = False
			client.session = None
			return
		if message != "":
			client.send_user_message(target=target, message=message)

def print_my_groups():
	print("Grupos que você é lider:")
	for group, attribute in client.groupHandler.groups.items():
		for key, value in attribute.items():
			if key =="lider" and value == user:
				print(f"\t - {group}")
	print("")

def print_active_groups():
	print("Grupos que você é membro:")
	for group, attribute in client.groupHandler.groups.items():
		if user in attribute["membros"]:
			if attribute["membros"][user] == "Aprovado":
				print(f"\t - {group}")
	print("")

def print_group_membership_requests(group):
	for user, status in client.groupHandler.groups.get(group).get("membros").items():
		if status == "Pendente":
			print(f"Usuário {user} solicitou entrada no grupo {group}")
	print("")


def gerenciar_grupo():
	with mutexTerminal:
		os.system('clear')
		print_my_groups()
		group = input("Informe o nome do grupo que deseja administrar ou \\voltar para voltar ao menu: ")
		if group == "\\voltar":
			return
		group = group.strip()
		if group != "":
			os.system('clear')
			print("Gerenciamento do grupo " + group)
			print("")
			print_group_membership_requests(group)
			user = input("Digite o nome do usuário que deseja aprovar ou \\voltar para voltar ao menu: ")
			if user == "\\voltar":
				return
			user = user.strip()
			if user != "":
				client.add_member(user=user, group=group)
				print("Usuário aprovado com sucesso")
				input("Pressione enter para voltar ao menu.")


user = input("Informe seu usuário: ")

user = user.strip()
if user == "":
	print("Usuário inválido")
	exit()

client = Client(user=user)
print("Inicializando...")
time.sleep(3)
client.subscribeActiveChats()

while True:
		os.system('clear')
		imprimirMenu()
		option = input("Digite a opção desejada: ")
		if option == "1":
			visualizar_usuarios()
		if option == "2":
			criar_grupo()
		if option == "3":
			visualizar_grupos()
		if option == "4":
			entrar_grupo()
		if option == "5":
			iniciar_conversa()
		if option == "6":
			visualizar_solicitacoes_conversa()
		if option == "7":
			aceitar_solicitacao_conversa()
		if option == "8":
			enviar_mensagem()
		if option == "9":
			gerenciar_grupo()
		if option == "10":
			client.logout()
			time.sleep(1)
			exit()