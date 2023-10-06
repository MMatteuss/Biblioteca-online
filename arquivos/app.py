from flask import Flask, render_template, request
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import sql

app = Flask(__name__)

db_config = {
    "dbname": "test",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

# ====== LOGIN ======
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        gmail = request.form.get('gmail')
        senha = request.form.get('senha')

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        query = sql.SQL("SELECT * FROM login WHERE gmail = %s AND senha = %s")
        cursor.execute(query, (gmail, senha))
        user = cursor.fetchone()

        if user:
            return render_template('home.html')
        else:
            return render_template('erro-index.html')

    return render_template('index.html')




# ====== CADASTRO ======
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        gmail = request.form['gmail']
        senha = request.form['senha']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("insert into login (gmail, senha) values (%s, %s)", (gmail, senha))
        
        conn.commit()
        cursor.close()
        return render_template('index.html')
    return render_template('cadastro.html')


# ==== usuarios cadastrados ======
@app.route('/uscad', methods=["GET","POST"])
def uscad():
    if request.method == 'POST':
        relatorio = request.form['relatorio']
        conexao = psycopg2.connect(**db_config)
        cursor = conexao.cursor()
        cursor.execute("SELECT gmail FROM login")
        result = cursor.fetchall()

        conexao.close()  # Fechando a conexão
        return render_template('us-cad.html', result=result)
        # return render_template('grid.html', result=result)
    else:
        return render_template('us-cad.html', result=None)


# ==== homepage =====
@app.route('/home', methods=["GET","POST"])
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)