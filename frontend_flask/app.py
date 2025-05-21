from flask import Flask, render_template, jsonify, request, redirect, session, url_for
import requests

app = Flask(__name__, template_folder="Home")
app.secret_key = 'segredo-super-seguro'

# Página inicial
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/inicial")
def inicial():
    return render_template("inicial.html")

@app.route("/adm")
def adm():
    return render_template("adm.html")

# API para buscar dados do backend Django
@app.route("/api/get_data", methods=["GET"])
def get_data():
    try:
        response = requests.get("http://localhost:8000/api/data/")
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API de login
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Aqui você pode integrar com Django ou usar um mock
    # Exemplo: autenticação mock
    if username == 'admin' and password == 'admin':
        session['username'] = username
        session['groups'] = ['admin']
        return jsonify({"success": True})
    # TODO: integrar autenticação real
    return jsonify({"success": False, "error": "Usuário ou senha inválidos"})

# API de cadastro
@app.route("/api/cadastro", methods=["POST"])
def api_cadastro():
    data = request.get_json()
    # Aqui você pode integrar com Django ou usar um mock
    # TODO: integração real
    return jsonify({"success": True})

# API para obter info do usuário logado
@app.route("/api/get_user_info", methods=["GET"])
def get_user_info():
    if 'username' in session:
        return jsonify({"username": session['username'], "groups": session.get('groups', [])})
    return jsonify({})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
