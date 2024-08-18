import tkinter as tk
from tkinter import filedialog
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sqlite3
import os
import createbd


def load_email_config():
    conn = sqlite3.connect('./BD/config.db')
    cursor = conn.cursor()
    cursor.execute('SELECT email, password, smtp_server, smtp_port FROM email_config ORDER BY id DESC LIMIT 1')
    config = cursor.fetchone()
    conn.close()
    if config:
        return {
            'email': config[0],
            'password': config[1],
            'smtp_server': config[2],
            'smtp_port': config[3]
        }
    else:
        return None
    

# Variáveis globais para armazenar os dados dos fornecedores e o caminho das medições
fornecedores_df = None
medicoes_dir = None

# Função para carregar fornecedores
def load_fornecedores():
    global fornecedores_df
    file_path = filedialog.askopenfilename()
    if file_path:
        fornecedores_df = pd.read_excel(file_path)
        label_fornecedores.config(
            text=f"Fornecedores: {os.path.basename(file_path)}")
    else:
        fornecedores_df = None


# Função para carregar arquivos de medição
def load_medicoes_dir():
    global medicoes_dir
    dir_path = filedialog.askdirectory()
    if dir_path:
        medicoes_dir = dir_path
        label_medicoes.config(text=f"Diretório de Medições: {dir_path}")
    else:
        medicoes_dir = None


def prepare_medicoes():
    global fornecedores_df
    if fornecedores_df is not None:
        if medicoes_dir:
            # Percorrer a lista de fornecedores
            for index, row in fornecedores_df.iterrows():
                nome_fornecedor = row['Nome']
                email_fornecedor = row['e-mail']

                # Procurar o arquivo de medição correspondente ao nome do fornecedor
                arquivo_medicao = os.path.join(
                    medicoes_dir, f"{nome_fornecedor}.xlsx")

                if os.path.isfile(arquivo_medicao):
                    # Carregar a tabela de medição do arquivo XLSX
                    tabela_medicao = pd.read_excel(arquivo_medicao)

                    # Armazenar as variáveis (exemplo de uso)
                    tabela = tabela_medicao
                    email = email_fornecedor

                    # Simular o envio do e-mail
                    send_email(email, tabela)
                else:
                    print(
                        f"Arquivo de medição não encontrado para: {nome_fornecedor}")
        else:
            print("Nenhum diretório de medições selecionado.")
    else:
        print("Nenhum fornecedor carregado.")

    #         # Exemplo de saída
    #         print(f"Fornecedor: {nome_fornecedor}")
    #         print(f"Email: {email}")
    #         print("Boletim de Medição:")
    #         print(tabela.head())  # Exibe as primeiras linhas da tabela
    #         print("-" * 40)


# Função para enviar email
def send_email(email, tabela):
    print(email)
    print(tabela)
    
    config = load_email_config()
    if config:
        print(f"Enviando e-mail usando {config['email']}")
        # Aqui você adicionaria o código para realmente enviar o e-mail, usando config['email'], config['password'], etc.
        
        # msg = MIMEMultipart()
        # msg['From'] = config['email']
        # msg['To'] = fornecedor['email']
        # msg['Subject'] = "Boletim de Medição"

        # body = config['body']
        # msg.attach(MIMEText(body, 'plain'))

        # attachment = open(file_path, "rb")
        # part = MIMEBase('application', 'octet-stream')
        # part.set_payload(attachment.read())
        # encoders.encode_base64(part)
        # part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(file_path)}")
        # msg.attach(part)

        # server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        # server.starttls()
        # server.login(config['email'], config['password'])
        # server.sendmail(config['email'], fornecedor['email'], msg.as_string())
        # server.quit()

    else:
        print("Configuração de e-mail não encontrada.")
        


# Configurações da interface gráfica
root = tk.Tk()
root.title("Envio de Boletim de Medição")
root.config(padx=10, pady=100)

def open_config_window():
    config_window = tk.Toplevel(root)
    config_window.title("Configurações de E-mail")

    tk.Label(config_window, text="E-mail Remetente:").grid(row=0, column=0)
    tk.Label(config_window, text="Servidor SMTP:").grid(row=1, column=0)
    tk.Label(config_window, text="Senha:").grid(row=2, column=0)
    tk.Label(config_window, text="Porta SMTP:").grid(row=3, column=0)

    email_entry = tk.Entry(config_window, width=30)
    email_entry.grid(row=0, column=1)
    smtp_server_entry = tk.Entry(config_window, width=30)
    smtp_server_entry.grid(row=1, column=1)
    password_entry = tk.Entry(config_window, show='*', width=30)
    password_entry.grid(row=2, column=1)
    smtp_port_entry = tk.Entry(config_window, width=30)
    smtp_port_entry.grid(row=3, column=1)

    def save_config():
        email = email_entry.get()
        password = password_entry.get()
        smtp_server = smtp_server_entry.get()
        smtp_port = smtp_port_entry.get()
        
        if not email or not password or not smtp_server or not smtp_port:
            print("Preencha todos os campos.")
            return
        
        if not smtp_port.isdigit():
            print("A porta SMTP deve ser um número inteiro.")
            return
        
        if not email.count('@') == 1 or not email.count('.') >= 1:
            print("E-mail inválido.")
            return
        
        
        # Quero verificar se o arquivo config.db existe, si não existir, chamar a função create_db
        if not os.path.isfile('./BD/config.db'):
            createbd.create_db()
        
        conn = sqlite3.connect('./BD/config.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO email_config (email, password, smtp_server, smtp_port)
            VALUES (?, ?, ?, ?)
        ''', (email, password, smtp_server, smtp_port))
        conn.commit()
        conn.close()

        config_window.destroy()

    save_button = tk.Button(config_window, text="Salvar", command=save_config)
    save_button.grid(row=4, column=1, columnspan=4)

# Adicionar o botão à interface principal
btn_open_config = tk.Button(root, text="Configurar E-mail", command=open_config_window)
btn_open_config.pack()

# Botões e interações da interface gráfica
btn_load_fornecedores = tk.Button(
    root, text="Carregar Fornecedores", command=load_fornecedores)
btn_load_fornecedores.pack()
# Labels para mostrar os arquivos selecionados
label_fornecedores = tk.Label(
    root, text="Fornecedores: Nenhum arquivo selecionado")
label_fornecedores.pack()

btn_load_medicoes = tk.Button(
    root, text="Selecionar Diretório de Medições", command=load_medicoes_dir)
btn_load_medicoes.pack()
label_medicoes = tk.Label(
    root, text="Diretório de Medições: Nenhum diretório selecionado")
label_medicoes.pack()

btn_enviar = tk.Button(root, text="Enviar Medição", command=prepare_medicoes)
btn_enviar.pack()

# Rodar a interface gráfica
root.mainloop()
