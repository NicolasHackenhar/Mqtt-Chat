import threading
import os
from src.Client import Client

mutexTerminal = threading.Lock()

def imprimirMenu():
	with mutexTerminal:
		print("Bem vindo ao chat")
		print(f"Você está logado como: {client.user}")
		print("1. Visualizar usuários")
		print("2. Criar grupo")
		print("3. Visualizar grupos")
		print("4. Iniciar conversa")
		print("5. Visualizar solicitações de conversa")
		print("6. Aceitar solicitação de conversa")
		print("7. Sair")
		print("")

def visualizar_usuarios():
	with mutexTerminal:
		os.system('clear')
		for user, status in client.statusHandler.userStatus.items():
				print(f"Usuário {user} está {status}")

		input("Pressione enter para voltar ao menu.")

def criar_grupo():
	with mutexTerminal:
		os.system('clear')
		name = input("Digite o nome do grupo: ")
		client.create_group(name=name)
		input("Pressione enter para voltar ao menu.")

def visualizar_grupos():
	with mutexTerminal:
		os.system('clear')
		for group, attribute in client.groupHandler.groups.items():
				print(f"Grupo {group}: ")
				for key, value in attribute.items():
					if key == "membros":
						print(f"\t{key}:")
						for memberName, addedAt in value.items():
							print(f"\t\t{memberName} adicionado {addedAt}")
					else:
						print(f"\t{key}: {value}")
				print("")
			
		input("Pressione enter para voltar ao menu.")

def iniciar_conversa():
	with mutexTerminal:
		#TODO: validar se já existe um chat ativo entre os usuários
		os.system('clear')
		user_target = input("Informe o usuário com quem deseja se comunicar:")
		client.new_chat(user_target=user_target)
		print("Solicitação enviada com sucesso")
		input("Pressione enter para voltar ao menu.")

def visualizar_solicitacoes_conversa():
	with mutexTerminal:
		os.system('clear')
		for user, attributes in client.chatHandler.pending_chats.items():
				print(f"Usuário: {user}")
				print(f"\tStatus: {attributes['status']}")
				print(f"\tSolicitado em: {attributes['criacao']}")
		for user, attributes in client.chatHandler.active_chats.items():
				print(f"Usuário: {user}")
				print(f"\tStatus: {attributes['status']}")
				print(f"\tIniciado em: {attributes['iniciado']}")
				print(f"\tTópico: {attributes['topic']}")	
			
		input("Pressione enter para voltar ao menu.")

def aceitar_solicitacao_conversa():
	with mutexTerminal:
		#TODO: validar se já existe um chat ativo entre os usuários
		os.system('clear')
		user_target = input("Informe o usuário com quem deseja se comunicar:")
		client.accept_chat(user_target=user_target)
		print("Solicitação enviada com sucesso")
		input("Pressione enter para voltar ao menu.")

user = input("Informe seu usuário: ")

client = Client(user=user)

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
			iniciar_conversa()
		if option == "5":
			visualizar_solicitacoes_conversa()
		if option == "6":
			aceitar_solicitacao_conversa()
		if option == "7":
			client.logout()
			exit()