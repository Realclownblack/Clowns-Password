import sqlite3
from PyQt5 import uic, QtWidgets,QtGui
from  hashlib import  md5
from PyQt5.QtCore import QTimer

class Telas_manager_password():
    def __init__(self):
        self.inicializar()

    def inicializar(self):
        self.tela_iniciador = uic.loadUi('Telas/Tela_Inicializadora.ui')
        self.tela_iniciador.show()
        self.tela_iniciador.login.clicked.connect(self.Fazer_login)
        self.tela_iniciador.register_2.clicked.connect(self.Fazer_register)
        self.tela_iniciador.sobre.clicked.connect(self.tela_sobre_app)

    def tela_sobre_app(self):
        self.tela_iniciador.hide()
        self.tela_sobre = uic.loadUi('Telas/Clowns_Password_sobre.ui')
        self.tela_sobre.show()
        self.tela_sobre.user_voltar.clicked.connect(self.voltar_sobre)

    def voltar_sobre(self):
        self.tela_sobre.hide()
        self.inicializar()

    def voltar_app(self):
        self.tela_principal.hide()
        exit()


    def Fazer_login(self):
        try:
            self.tela_iniciador.hide()
        except:
            pass
        self.tela_login = uic.loadUi('Telas/Clowns_Password_Login.ui')
        self.tela_login.show()
        self.tela_login.input_user_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.tela_login.enviado_dados.clicked.connect(self.login_user)
        self.tela_login.user_voltar.clicked.connect(self.voltar_login)
        self.tela_login.esqueci_senha.clicked.connect(self.recuperar_password)

    def login_user(self):

        self.data_bese_users2 = sqlite3.connect("DATABASE/users_databese.db")
        self.cusor_users2 = self.data_bese_users2.cursor()

        ''' criando hash username'''
        self.hash_name = self.tela_login.input_user_name.text()
        self.hash_name = self.hash_name.encode("utf8")
        self.hash_name_hash = md5(self.hash_name).hexdigest()

        ''' criando hash password'''
        self.hash_password = self.tela_login.input_user_password.text()
        self.hash_password = self.hash_password.encode("utf8")
        self.hash_password = md5(self.hash_password).hexdigest()

        self.cusor_users2.execute(f"SELECT passwords FROM users WHERE username ='{self.hash_name_hash}'")
        self.vindo_databese_password = self.cusor_users2.fetchall()
        if self.hash_password == self.vindo_databese_password[0][0]:
            self.tela_login.senha_user_invalido.setText("successfully connect")
            self.tela_login.input_user_password.clear()
            self.create_database(f"{self.hash_name_hash}")
        else:
            self.tela_login.senha_user_invalido.setText("Invalid password or users")
            self.tela_login.input_user_password.clear()
        self.cusor_users2.close()

    def recuperar_password(self):
        self.tela_recuoeracao = uic.loadUi("Telas/Clowns_Password_salvo.ui")
        self.tela_recuoeracao.show()
        self.tela_recuoeracao.enviar_codigo_email.clicked.connect(self.eviar_codigo)
        self.tela_recuoeracao.enviar_email_2.setText("user name")
        self.tela_recuoeracao.verificador.clicked.connect(self.verifacar_codigo)

    def eviar_codigo(self):
        self.data_bese_users2 = sqlite3.connect("DATABASE/users_databese.db")
        self.cusor_users2 = self.data_bese_users2.cursor()

        ''' criando hash username'''
        self.hash_name = self.tela_recuoeracao.user_enviar_codigo.text()
        self.hash_name = self.hash_name.encode("utf8")
        self.hash_name_verificar = md5(self.hash_name).hexdigest()

        self.cusor_users2.execute(f"SELECT email FROM users WHERE username ='{self.hash_name_verificar}'")
        self.vindo_databese_email = self.cusor_users2.fetchall()
        if(self.vindo_databese_email == []):
            self.tela_recuoeracao.enviar_email.setText("user invalido")
        else:
            self.tela_recuoeracao.enviar_email.setText("codigo enviado para email")
            self.tela_recuoeracao.enviar_email_2.setText(self.vindo_databese_email[0][0])

    def verifacar_codigo(self):

        if self.tela_recuoeracao.codigo_trocar_senha.text() == "3255":
            self.tela_recuoeracao.text_informa.setText("validated code")
            self.add_password()
        else:
            self.tela_recuoeracao.text_informa.setText("code not validated")
            pass

    def add_password(self):
        self.tela_recuoeracao.hide()
        self.tela_add_password = uic.loadUi("Telas/Clowns_Password_novo_password.ui")
        self.tela_add_password.show()
        self.tela_add_password.enviar_nova_senha.clicked.connect(self.verificar_nova_password)
        self.tela_add_password.novo_password_1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.tela_add_password.novo_password_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.tela_add_password.notificacao.setText("Enter the new password")

    def verificar_nova_password(self):
        self.senhanova1 =  self.tela_add_password.novo_password_1.text()
        self.senhanova2 = self.tela_add_password.novo_password_2.text()

        if self.senhanova1 == self.senhanova2:

            ''' criando hash password'''
            self.hash_password_nov = self.senhanova1
            self.hash_password_nov = self.hash_password_nov.encode("utf8")
            self.hash_password_novo1 = md5(self.hash_password_nov).hexdigest()

            ''' criando hash username'''
            self.hash_name = self.tela_recuoeracao.user_enviar_codigo.text()
            self.hash_name = self.hash_name.encode("utf8")
            self.hash_name_verificar = md5(self.hash_name).hexdigest()

            '''dando updata no banco dedados'''
            self.cusor_users2.execute(f"UPDATE users SET passwords='{self.hash_password_novo1}' WHERE username='{self.hash_name_verificar}'")
            self.data_bese_users2.commit()
            self.tela_add_password.hide()

        else:
            pass

    def Fazer_register(self):
        self.tela_iniciador.hide()
        self.tela_register = uic.loadUi('Telas/Clowns_Password_Register.ui')
        self.tela_register.show()
        self.tela_register.input_novo_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.tela_register.user_voltar.clicked.connect(self.voltar_register)
        self.tela_register.carregando_dados_register.clicked.connect(self.save_databese_user)


    def voltar_register(self):
        self.tela_register.hide()
        self.inicializar()

    def voltar_login(self):
        self.inicializar()
        self.tela_login.hide()

    def voltar_cadastros(self):
        self.tela_cadastro_pass.hide()
        self.tela_principal_app()

    def create_database(self,database_name):
        try:
            self.data_bese_service = sqlite3.connect(f'DATABASE/{database_name}.db')
        except sqlite3.Error:
            pass
        self.data_service_name = database_name

        self.tela_principal_app()

    def save_databese_user(self):
        try:
            self.data_bese_users = sqlite3.connect("DATABASE/users_databese.db")

        except sqlite3.Error:
            pass
        try:
            self.data_bese_users.execute("CREATE TABLE users (username text,passwords text ,email text)")

        except sqlite3.Error:
            pass
        self.cusor_users = self.data_bese_users.cursor()

        ''' criando hash username'''
        self.hash_name_databese = self.tela_register.input_novo_user_name.text()
        self.hash_name_databese = self.hash_name_databese.encode("utf8")
        self.hash_name_databese = md5(self.hash_name_databese).hexdigest()

        ''' criando hash password'''
        self.hash_password_databese = self.tela_register.input_novo_password.text()
        self.hash_password_databese = self.hash_password_databese.encode("utf8")
        self.hash_password_databese = md5(self.hash_password_databese).hexdigest()

        ''' criando  email'''
        self.hash_email_databese = self.tela_register.input_email.text()

        self.cusor_users.execute(f"INSERT INTO users VALUES('{self.hash_name_databese}','{self.hash_password_databese}','{self.hash_email_databese}')")
        self.data_bese_users.commit()
        self.inicializar()
        self.tela_register.hide()

    def tela_principal_app(self):
        self.tela_login.hide()
        self.tela_principal = uic.loadUi('Telas/Clowns_Password_app.ui')
        self.tela_principal.show()
        self.service_lista()

        self.tela_principal.password_leberar_acesso.setEchoMode(QtWidgets.QLineEdit.Password)

        self.tela_principal.user_habilitar.move(300, 300)
        self.tela_principal.user_habilitar.resize(21, 21)
        self.tela_principal.user_habilitar.setPixmap(QtGui.QPixmap('img/esconder.png'))

        self.tela_principal.exit_app.clicked.connect(self.voltar_app)
        self.tela_principal.salvar_nova_senha.clicked.connect(self.tela_casdatro_password)
        self.tela_principal.nao_listado.addItems(self.lista_service)
        self.tela_principal.autenticar.clicked.connect(self.verificar_liberar)

    def verificar_liberar(self):

        ''' criando hash password'''
        self.hash_password_habilitar = self.tela_principal.password_leberar_acesso.text()
        self.hash_password_habilitar = self.hash_password_habilitar.encode("utf8")
        self.hash_password_habilitar = md5(self.hash_password_habilitar).hexdigest()

        if self.hash_password_habilitar == self.vindo_databese_password[0][0]:
            self.tela_principal.noti_liberar.clear()
            self.liberar_password()
        else:
            self.tela_principal.password_leberar_acesso.clear()
            self.tela_principal.noti_liberar.setText('Password invalid')

    def liberar_password(self):
        self.service_selecionado = self.tela_principal.nao_listado.currentText()
        self.cusor_service1.execute(f"SELECT * FROM service WHERE ServiceName='{self.service_selecionado}'")
        self.service_selecionada = self.cusor_service1.fetchall()
        self.lista_dados = []
        for service__ in range(len(self.service_selecionada)):
            self.lista_dados.append(self.service_selecionada)

        name_service = f'{self.lista_dados[0][0][0]}'
        user_service = f'{self.lista_dados[0][0][1]}'
        password_service = f'{self.lista_dados[0][0][2]}'

        self.tela_principal.user_habilitar.move(300, 300)
        self.tela_principal.user_habilitar.resize(21, 21)
        self.tela_principal.user_habilitar.setPixmap(QtGui.QPixmap('img/visualizar.png'))

        self.tela_principal.password_leberar_acesso.setEnabled(False)
        self.tela_principal.autenticar.setEnabled(False)

        self.tela_principal.acesso_login.setText(f"{name_service}")
        self.tela_principal.acesso_password.setText(f"{user_service}")
        self.tela_principal.text_leberar.setText(f"{password_service}")
        self.tela_principal.password_leberar_acesso.clear()

        self.time = QTimer()
        self.time.start(10000)
        self.time.timeout.connect(lambda: self.clear_password())


    def clear_password(self):

        self.tela_principal.user_habilitar.move(300, 300)
        self.tela_principal.user_habilitar.resize(21, 21)
        self.tela_principal.user_habilitar.setPixmap(QtGui.QPixmap('img/esconder.png'))

        self.tela_principal.password_leberar_acesso.setEnabled(True)
        self.tela_principal.autenticar.setEnabled(True)

        self.tela_principal.acesso_login.clear()
        self.tela_principal.acesso_password.clear()
        self.tela_principal.text_leberar.clear()

    def service_lista(self):
        self.cadastro_service_login()
        self.lista_service = ['Empty']
        try:
            self.data_bese_service1 = sqlite3.connect(f'DATABASE/{self.hash_name_hash}.db')
            self.cusor_service1 = self.data_bese_service1.cursor()
        except sqlite3.Error:
            pass
        self.cusor_service1.execute(f"SELECT ServiceName FROM service")
        self.services = self.cusor_service1.fetchall()
        for service in self.services:
            self.lista_service.append(service[0])
        if len(self.lista_service) == 1:
            return self.lista_service
        else:
            return self.lista_service.pop(0)


    def tela_casdatro_password(self):

        self.tela_principal.hide()
        self.tela_cadastro_pass = uic.loadUi('Telas/Clowns_Password_cadastro.ui')
        self.tela_cadastro_pass.show()
        self.tela_cadastro_pass.user_voltar.clicked.connect(self.voltar_cadastros)
        self.tela_cadastro_pass.salvar_dados.clicked.connect(self.cadastro_service)
        self.tela_cadastro_pass.service_password.setEchoMode(QtWidgets.QLineEdit.Password)


    def cadastro_service_login(self):
        self.data_bese_service = sqlite3.connect(f'DATABASE/{self.data_service_name}.db')
        self.cusor_service = self.data_bese_service.cursor()
        try:
            self.login_user = self.tela_login.input_user_name.text()
            self.password_user = self.tela_login.input_user_password.text()

            self.data_bese_service.execute("CREATE TABLE service (ServiceName text, serviceuser text ,servicepassword text)")
            query_login = f"INSERT INTO service VALUES('Manager_Password','{self.login_user}','{self.password_user}')"
            self.cusor_service.execute(query_login)
            self.data_bese_service.commit()
        except sqlite3.Error:
            pass

    def cadastro_service(self):

        self.data_bese_service = sqlite3.connect(f'DATABASE/{self.data_service_name}.db')
        self.cusor_service = self.data_bese_service.cursor()
        try:
            self.data_bese_service.execute("CREATE TABLE service (ServiceName text, serviceuser text ,servicepassword text)")

        except sqlite3.Error:
            pass
        self.service_name = self.tela_cadastro_pass.service_name.text()
        self.sevice_user = self.tela_cadastro_pass.service_user.text()
        self.sevice_password = self.tela_cadastro_pass.service_password.text()

        self.service_insert()

    def service_insert(self):
        try:
            query = f"INSERT INTO service VALUES('{self.service_name}','{self.sevice_user}','{self.sevice_password}')"
            query_login = f"INSERT INTO service VALUES('Manager_Password','{self.login_user}','{self.password_user}')"
            self.cusor_service.execute(query_login)
            self.cusor_service.execute(query)
            self.data_bese_service.commit()
        except sqlite3.Error:
            pass
        self.tela_cadastro_pass.hide()
        self.tela_principal_app()

