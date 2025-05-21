from flask import Flask, render_template, jsonify, request, redirect, session, url_for
import requests
import os

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
    if 'username' not in session:
        return redirect('/login')
    return render_template("inicial.html", username=session['username'], groups=session.get('groups', []), permissions=session.get('permissions', []))

@app.route("/adm")
def adm():
    return render_template("adm.html")

@app.route("/adm/usuarios")
def adm_usuarios():
    return render_template("adm_usuarios.html")

@app.route("/adm/grupos")
def adm_grupos():
    return render_template("adm_grupos.html")

@app.route("/adm/arquivos")
def adm_arquivos():
    return render_template("adm_arquivos.html")

@app.route("/adm/banco")
def adm_banco():
    return render_template("adm_banco.html")

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
    try:
        # Verifica autenticação no backend Django
        r = requests.post("http://localhost:8000/api/login/", json={"username": username, "password": password})
        resp = r.json()
        if resp.get("success"):
            session['username'] = username
            session['groups'] = resp.get('groups', [])
            session['permissions'] = resp.get('permissions', [])
            return jsonify({"success": True, "redirect": "/inicial"})
        else:
            return jsonify({"success": False, "error": resp.get("error", "Usuário ou senha inválidos")})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# API de cadastro
@app.route("/api/cadastro", methods=["POST"])
def api_cadastro():
    data = request.get_json()
    try:
        # Envia para o backend Django
        r = requests.post("http://localhost:8000/api/criar_usuario/", json=data)
        resp = r.json()
        if resp.get("success"):
            return jsonify({"success": True, "redirect": "/login"})
        else:
            return jsonify({"success": False, "error": resp.get("error", "Erro ao cadastrar")})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# API para obter info do usuário logado
@app.route("/api/get_user_info", methods=["GET"])
def get_user_info():
    if 'username' in session:
        return jsonify({"username": session['username'], "groups": session.get('groups', [])})
    return jsonify({})

# API para listar usuários do Django
@app.route("/api/usuarios", methods=["GET"])
def api_usuarios():
    try:
        r = requests.get("http://localhost:8000/api/usuarios/")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})

# API para listar grupos do Django
@app.route("/api/grupos", methods=["GET"])
def api_grupos():
    try:
        r = requests.get("http://localhost:8000/api/grupos/")
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})

# API para ver código fonte (apenas leitura)
@app.route("/api/codigo", methods=["GET"])
def api_codigo():
    path = request.args.get('path', 'app.py')
    try:
        with open(f'../aula_12-03-2025/P-S-E_pycharm/SecretariaEscolar/projeto/{path}', 'r', encoding='utf-8') as f:
            return jsonify({"codigo": f.read()})
    except Exception as e:
        return jsonify({"error": str(e)})

# API para ver banco de dados (apenas leitura)
@app.route("/api/banco", methods=["GET"])
def api_banco():
    try:
        import sqlite3
        conn = sqlite3.connect('../aula_12-03-2025/P-S-E_pycharm/SecretariaEscolar/db.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        db = {}
        for t in tables:
            table = t[0]
            cursor.execute(f'SELECT * FROM {table} LIMIT 20')
            db[table] = cursor.fetchall()
        conn.close()
        return jsonify(db)
    except Exception as e:
        return jsonify({"error": str(e)})

# --- API para criar usuário ---
@app.route("/api/criar_usuario", methods=["POST"])
def criar_usuario():
    data = request.get_json()
    try:
        r = requests.post("http://localhost:8000/api/criar_usuario/", json=data)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})

# --- API para criar grupo ---
@app.route("/api/criar_grupo", methods=["POST"])
def criar_grupo():
    data = request.get_json()
    try:
        r = requests.post("http://localhost:8000/api/criar_grupo/", json=data)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})

# --- API para listar arquivos do backend ---
@app.route("/api/listar_arquivos", methods=["GET"])
def listar_arquivos():
    pasta = request.args.get('pasta', '../aula_12-03-2025/P-S-E_pycharm/SecretariaEscolar/projeto')
    try:
        arquivos = [f for f in os.listdir(pasta) if os.path.isfile(os.path.join(pasta, f))]
        return jsonify({"arquivos": arquivos})
    except Exception as e:
        return jsonify({"error": str(e)})

# --- API para pesquisar no banco de dados ---
@app.route("/api/pesquisar_banco", methods=["POST"])
def pesquisar_banco():
    data = request.get_json()
    tabela = data.get('tabela')
    termo = data.get('termo')
    try:
        import sqlite3
        conn = sqlite3.connect('../aula_12-03-2025/P-S-E_pycharm/SecretariaEscolar/db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = [col[1] for col in cursor.fetchall()]
        query = f"SELECT * FROM {tabela} WHERE " + " OR ".join([f"{col} LIKE ?" for col in colunas])
        params = [f"%{termo}%"] * len(colunas)
        cursor.execute(query, params)
        resultados = cursor.fetchall()
        conn.close()
        return jsonify({"resultados": resultados, "colunas": colunas})
    except Exception as e:
        return jsonify({"error": str(e)})

# --- API para editar banco de dados (update simples) ---
@app.route("/api/editar_banco", methods=["POST"])
def editar_banco():
    data = request.get_json()
    tabela = data.get('tabela')
    pk_col = data.get('pk_col')
    pk_val = data.get('pk_val')
    campo = data.get('campo')
    novo_valor = data.get('novo_valor')
    try:
        import sqlite3
        conn = sqlite3.connect('../aula_12-03-2025/P-S-E_pycharm/SecretariaEscolar/db.sqlite3')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {tabela} SET {campo}=? WHERE {pk_col}=?", (novo_valor, pk_val))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
