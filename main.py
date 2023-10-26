import threading
import os
from src.LoginPublisher import LoginPublisher
from src.UsersSubscriber import UsersSubscriber
from src.GroupPublisher import GroupPublisher
from src.GroupSubscriber import GroupSubscriber
from src.ChatPublisher import ChatPublisher
from src.ChatSubscriber import ChatSubscriber

#TODO: Adicionar funcionalidade para juntar-se a grupo
#TODO: Adicionar funcionalidade para aceitar solicitação de conversa
#TODO: Abstrair o Client usando em todas as classes para um client só (passar como parâmetro para as demais)
#TODO: Classes de Subscriber e Publisher vão somente tratar as mensagens
#TODO: Juntar todos os on_message em um método só da classe Client

mutexUserStatus = threading.Lock()
mutexGroupSubscriber = threading.Lock()
mutextChatRequests = threading.Lock()
mutexTerminal = threading.Lock()

user = input("Informe seu usuário: ")

loginPublisher = LoginPublisher(user=user)
loginPublisher.login()

usersSubscriber = UsersSubscriber(user=user, mutexUserStatus=mutexUserStatus)
groupSubscriber = GroupSubscriber(user=user, mutexGroupSubscriber=mutexGroupSubscriber)
chatPublisher = ChatPublisher(user=user)
chatSubscriber = ChatSubscriber(user=user)

chats = {}


def imprimirMenu():
	with mutexTerminal:
		print("Bem vindo ao chat")
		print("1. Visualizar usuários")
		print("2. Criar grupo")
		print("3. Visualizar grupos")
		print("4. Iniciar conversa")
		print("5. Visualizar solicitações de conversa")
		print("6. Aceitar solicitação de conversa")
		print("7. Sair")
		print("")
		
def consultar_status_usuarios():
	while True:
		usersSubscriber.show_users()

def consultar_grupos():
	while True:
		groupSubscriber.show_groups()

def consultar_solicitacoes_conversa():
	while True:
		chatSubscriber.show_chat_requests()

def visualizar_usuarios():
	with mutexTerminal:
		os.system('clear')
		with mutexUserStatus:
			for user, status in usersSubscriber.userStatus.items():
				print(f"Usuário {user} está {status}")

		input("Pressione enter para voltar ao menu.")

def visualizar_grupos():
	with mutexTerminal:
		os.system('clear')
		with mutexGroupSubscriber:
			for group, attribute in groupSubscriber.groups.items():
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
	
def criar_grupo():
	with mutexTerminal:
		os.system('clear')
		groupName = input("Digite o nome do grupo: ")
		groupPublisher = GroupPublisher(user=user, groupName=groupName)
		groupPublisher.create()
		groupPublisher.add_member()
		input("Pressione enter para voltar ao menu.")

def iniciar_conversa():
	with mutexTerminal:
		#TODO: validar se já existe um chat ativo entre os usuários
		os.system('clear')
		userTarget = input("Informe o usuário com quem deseja se comunicar:")
		chatPublisher.newCoversation(userTarget=userTarget)
		print("Solicitação enviada com sucesso")
		input("Pressione enter para voltar ao menu.")

def aceitar_solicitacao_conversa():
	with mutexTerminal:
		#TODO: validar se já existe um chat ativo entre os usuários
		os.system('clear')
		userTarget = input("Informe o usuário com quem deseja se comunicar:")
		chatPublisher.acceptConversation(userTarget=userTarget)
		print("Solicitação enviada com sucesso")
		input("Pressione enter para voltar ao menu.")

def visualizar_solicitacoes_conversa():
	with mutexTerminal:
		os.system('clear')
		with mutextChatRequests:
			for user, attributes in chatSubscriber.chats.items():
				print(f"Usuário: {user}")
				print(f"\tStatus: {attributes['status']}")
				print(f"\tSolicitado em: {attributes['criacao']}")
		input("Pressione enter para voltar ao menu.")


thread_consulta_usuarios = threading.Thread(target=consultar_status_usuarios, daemon=True)
thread_consulta_grupos = threading.Thread(target=consultar_grupos, daemon=True)
thread_consulta_requisicoes_chat = threading.Thread(target=consultar_solicitacoes_conversa, daemon=True)

thread_consulta_usuarios.start()
thread_consulta_grupos.start()
thread_consulta_requisicoes_chat.start()

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
			loginPublisher.logout()
			exit()
		

