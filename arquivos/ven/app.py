from flask import Flask, render_template, request, flash, request, redirect, url_for
import psycopg2
from psycopg2 import sql
from werkzeug.utils import secure_filename


app = Flask(__name__)

banco = {
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

        conn = psycopg2.connect(**banco)
        cursor = conn.cursor()

        query = sql.SQL("SELECT * FROM login WHERE gmail = %s AND senha = %s")
        cursor.execute(query, (gmail, senha))
        user = cursor.fetchone()

        if user:
            return render_template('home.html')
        else:
            return render_template('erro-index.html')

    return render_template('index.html')


# Cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastroUsuario():
    if request.method == "POST":
        gmail = request.form.get('gmail')
        senha = request.form.get('senha')
        nome = request.form.get('nome')

        conn = psycopg2.connect(**banco)
        cursor = conn.cursor()

        cursor.execute(sql.SQL("INSERT INTO login (gmail, senha, nome) values (%s, %s, %s)"), (gmail, senha, nome))
        conn.commit()

        cursor.close()  # Fechando o cursor
        conn.close()  # Fechando a conexão

        if(cursor):
            return index()

    return render_template('cadastro.html')


# termos de privacidade
@app.route('/termosdeprivacidade')
def termosdeprivacidade():
    return render_template('/termos-de-privacidade.html')


# termos de licensa
@app.route('/termosdelicensa')
def termosdelicensa():
    return render_template('/termos-de-licensa.html')


@app.route('/home', methods=["GET", "POST"])
def home():
    return render_template('home.html')


#===== cadastro do usuario =======
@app.route('/uscad', methods=['GET', 'POST'])
def uscad():
    if request.method == 'POST':
        relatorio = request.form['relatorio']

        conexao = psycopg2.connect(**banco)
        cursor = conexao.cursor()
        cursor.execute("SELECT gmail FROM login")
        result = cursor.fetchall()

        conexao.close()  # Fechando a conexão
        return render_template('us-cad.html', result=result)
    else:
        return render_template('us-cad.html', result=None)



#===== pdfs =======
@app.route('/pdfs', methods=['GET', 'POST'])
def pdfs():
    if request.method == 'POST':
        relatorio = request.form['relatorio']
        conexao = psycopg2.connect(**banco)
        cursor = conexao.cursor()
        cursor.execute("SELECT nome_pdf, arquivo_pdf FROM pdf")
        result = cursor.fetchall()

        conexao.close()  # Fechando a conexão
        return render_template('pdfs.html', result=result)
    else:
        return render_template('pdfs.html', result=None)


# @app.route('/<nomeDesconhecido>' or '/termosdeprivacidade/<nomeDesconhecido>' or '/home/Cadastro<nomeDesconhecido>' or '/uscad/<nomeDesconhecido>' or '/pdfs/<nomeDesconhecido>')
# def nomeDesconhecido(nomeDesconhecido):
#     return render_template('erro.html')

if __name__ == '__main__':
    app.run(debug=True)