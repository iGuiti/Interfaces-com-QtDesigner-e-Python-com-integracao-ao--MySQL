import re
import sys
import os
from PyQt5 import QtWidgets, uic
import mysql.connector
import resources_rc
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QIcon

# Conexão com o host e o data base que irão armazenar os dados
conexao = mysql.connector.connect(
    host = 'localhost',
    user = 'dev',
    password = '3013',
    database = 'Clientes_Connect'
)
num_id = 0

def validar(cpf,nome,telefone,aparelho):

     # Verifica se os campos estão vazios
    if not cpf or not nome or not telefone or not aparelho:
        return "Todos os campos devem estar preenchidos."

    # Verifica se o CPF contém apenas números (usando regex)
    if not re.match("^[0-9]{11}$", cpf):
        return "O CPF deve conter exatamente 11 números."

    # Verifica se o telefone contém apenas números (você pode ajustar conforme a necessidade)
    if not re.match("^[0-9]+$", telefone):
        return "O telefone deve conter apenas números."
    
    return None
    
# Função para realizar buscas no banco pelo cpf cadastrado
def buscar ():
    cursor = conexao.cursor()
    Buscar_cpf = lista.txtBuscarCpf.text()
    dados = (str(Buscar_cpf))
    comandos_sql = 'select * from clientes'
    if not Buscar_cpf: 
        cursor.execute(comandos_sql)
    else:
        cursor.execute('select * from clientes where cpf = '+str(dados))
    leituraBanco = cursor.fetchall()
    lista.tableWidget.setRowCount(len(leituraBanco))
    lista.tableWidget.setColumnCount(5)

    for i in range (0, len(leituraBanco)):
        for j in range (0, 5):
            lista.tableWidget.setItem(i , j, QtWidgets.QTableWidgetItem(str(leituraBanco[i][j])))

    lista.txtBuscarCpf.setText('')

# Função para deletar cadastros do banco
def delete():
    remover = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(remover)
    cursor = conexao.cursor()
    cursor.execute('select CPF from clientes')
    leitura_banco = cursor.fetchall()
    valor_cpf = leitura_banco [remover][0]
    cursor.execute('Delete from clientes where cpf = %s',(valor_cpf,))
    lista.lblApagado.setText('CADASTRO APAGADO!')
    conexao.commit()

# Função para abrir a UI 'Alterar' resgatando a linha(Row) ativa na lista 
def editar():
    global num_id
    dados = lista.tableWidget.currentRow()
    cursor = conexao.cursor()
    cursor.execute('select CPF from clientes')
    leitura_banco = cursor.fetchall()
    valor_cpf = leitura_banco [dados][0]
    cursor.execute('select * from clientes where cpf = '+str(valor_cpf))
    leitura_banco = cursor.fetchall()     

    Alterar.show()

    num_id = valor_cpf
    Alterar.txtAltCpf.setText(str(leitura_banco[0][0]))
    Alterar.txtAltCliente.setText(str(leitura_banco[0][1]))
    Alterar.txtAltFone.setText(str(leitura_banco[0][2]))
    Alterar.txtAltAparelho.setText(str(leitura_banco[0][3]))

# Função do botão 'Confirmar' para confirmar alterações no banco
def Confirmar_alteracoes():
    global num_id
    cpf = Alterar.txtAltCpf.text()
    nome = Alterar.txtAltCliente.text()
    telefone = Alterar.txtAltFone.text()
    aparelho = Alterar.txtAltAparelho.text()
    finalizados = ''
    cursor = conexao.cursor()
    if Alterar.btnFim.isChecked():
         cursor.execute("update clientes set cpf='{}', nome='{}', telefone='{}', aparelho='{}', finalizados='Sim' where cpf={}".format(cpf, nome, telefone, aparelho, num_id))
    else:
        cursor.execute("update clientes set cpf='{}', nome='{}', telefone='{}', aparelho='{}', finalizados='' where cpf={}".format(cpf, nome, telefone, aparelho, num_id))
    Alterar.lblAlteracao.setText('ALTERAÇÃO SALVA!')
    conexao.commit()
    
# Função para abrir a UI lista, atribuida ao botão "Relatório"
def listar():
    lista.show()


    lista.tableWidget.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
    lista.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    lista.tableWidget.verticalHeader().setVisible(False)
    
    cursor = conexao.cursor()
    comandos_SQL = 'select * from clientes'
    cursor.execute(comandos_SQL)
    leituraBanco = cursor.fetchall()

    lista.tableWidget.setRowCount(len(leituraBanco))
    lista.tableWidget.setColumnCount(5)

    for i in range (0, len(leituraBanco)):
        for j in range (0, 5):
            lista.tableWidget.setItem(i , j, QtWidgets.QTableWidgetItem(str(leituraBanco[i][j])))

# Função para inserir dados no banco
def insert():
    cpf = Formulario.txtCpf.text()
    nome = Formulario.txtCliente.text()
    telefone = Formulario.txtFone.text()
    aparelho = Formulario.txtAparelho.text()

    erro = validar(cpf,nome,telefone,aparelho)
    if erro:
        Formulario.lblConfirmar.setStyleSheet("color: red; font-weight: bold;")
        Formulario.lblConfirmar.setText(erro)
        return
    cursor = conexao.cursor()
    comandos_Sql = 'insert into clientes (cpf, nome, telefone, aparelho) values (%s, %s, %s, %s)'
    dados = (str(cpf), str(nome), str(telefone), str(aparelho))
    cursor.execute(comandos_Sql, dados)
    conexao.commit()

    Formulario.txtCpf.setText('')
    Formulario.txtCliente.setText('')
    Formulario.txtFone.setText('')
    Formulario.txtAparelho.setText('')
    Formulario.lblConfirmar.setStyleSheet("color: green; font-weight: bold;")
    Formulario.lblConfirmar.setText("DADOS INSERIDOS!")

def caminho_arquivo(nome):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, nome)
    return os.path.join(os.path.abspath("."), nome)

# Aplicação para carregar e abrir as interfaces (UI)
app = QtWidgets.QApplication([])
Formulario = uic.loadUi(caminho_arquivo('FormCNN.ui'))
lista = uic.loadUi(caminho_arquivo('lista.ui'))
Alterar = uic.loadUi(caminho_arquivo('alterar.ui'))
app.setWindowIcon(QIcon(caminho_arquivo('icone_logo.ico')))

# Aplicação para dar funcionalidade aos botões(Btn), chamando as funções que eles devem executar
Formulario.btnCadastrar.clicked.connect(insert)
Formulario.btnRelatorio.clicked.connect(listar)
lista.btnAtt.clicked.connect(editar)
lista.btnApagar.clicked.connect(delete)
lista.btnBuscar.clicked.connect(buscar)
Alterar.btnConfirmar.clicked.connect(Confirmar_alteracoes)
# Exibir tela principal e executar os wigets
Formulario.show()
app.exec()