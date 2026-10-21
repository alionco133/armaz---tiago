import json
import os
from flask import Flask, render_template_string, request

app = Flask(__name__)

ARQUIVO_USUARIOS = 'usuarios.json'

# Função para ler os usuários do arquivo JSON
def carregar_usuarios():
    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Função para salvar novos usuários no arquivo JSON
def salvar_usuarios(usuarios):
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=4)

HTML_TELA = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Sistema de Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="POST" action="/">
        <input type="text" name="usuario" placeholder="Usuário" required><br><br>
        <input type="password" name="senha" placeholder="Senha" required><br><br>
        <button type="submit">Entrar</button>
    </form>

    <hr>

    <h2>Cadastrar Novo Usuário</h2>
    <form method="POST" action="/cadastrar">
        <input type="text" name="novo_usuario" placeholder="Novo Usuário" required><br><br>
        <input type="password" name="nova_senha" placeholder="Nova Senha" required><br><br>
        <button type="submit">Cadastrar</button>
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        usuarios = carregar_usuarios()

        if usuario in usuarios and usuarios[usuario] == senha:
            return f"<h1>Sucesso! Bem-vindo, {usuario}.</h1>"
        else:
            return "<h1>Falha! Usuário ou senha incorretos.</h1><a href='/'>Tentar de novo</a>"

    return render_template_string(HTML_TELA)

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    novo_usuario = request.form['novo_usuario']
    nova_senha = request.form['nova_senha']

    usuarios = carregar_usuarios()

    if novo_usuario in usuarios:
        return "<h1>Erro: Usuário já existe!</h1><a href='/'>Voltar</a>"

    # Adiciona o novo usuário e salva no arquivo usuarios.json
    usuarios[novo_usuario] = nova_senha
    salvar_usuarios(usuarios)

    return f"<h1>Usuário {novo_usuario} cadastrado com sucesso!</h1><a href='/'>Ir para o Login</a>"

if __name__ == '__main__':
    app.run(debug=True)