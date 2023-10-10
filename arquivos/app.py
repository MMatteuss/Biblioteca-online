from flask import Flask, render_template, request, flash, request, redirect, url_for
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from psycopg2 import sql
import os
from werkzeug.utils import secure_filename
from flask import send_from_directory, jsonify
# import binascii


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
        conexao = psycopg2.connect(**db_config)
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, gmail FROM login")
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
        conexao = psycopg2.connect(**db_config)
        cursor = conexao.cursor()
        cursor.execute("SELECT nome_pdf, arquivo_pdf FROM pdf")
        result = cursor.fetchall()

        conexao.close()  # Fechando a conexão
        return render_template('pdfs.html', result=result)
    else:
        return render_template('pdfs.html', result=None)




# @app.route('/pdfs-2', methods=['GET', 'POST'])
# def pdfss():
#     if request.method == 'POST':
#         relatorio = request.form['relatorio']
#         conexao = psycopg2.connect(**db_config)
#         cursor = conexao.cursor()
#         cursor.execute("SELECT arquivo_pdf FROM pdf")
#         result = cursor.fetchall()

#         conexao.close()  # Fechando a conexão
#         return render_template('pdfs-2.html', result=result)
#     else:
#         return render_template('pdfs-2.html', result=None)



# @app.route('/pdfs-4', methods=['GET', 'POST'])
# def pdfsss():
#     if request.method == 'POST':
#         relatorio = request.form['relatorio']
#         conexao = psycopg2.connect(**db_config)
#         cursor = conexao.cursor()
#         cursor.execute("SELECT arquivo_pdf FROM pdf")
#         result = cursor.fetchall()

#         conexao.close()  # Fechando a conexão
#         return render_template('pdfs-2.html')
#     else:
#         return render_template('pdfs-2.html', result=None)
 














# ===== test =====
# conexao = psycopg2.connect(**db_config)
# cursor = conexao.cursor()
# cursor.execute("insert into nome_pdf, arquivo_pdf FROM pdf")
# UPLOAD_FOLDER = './data'


# ALLOWED_EXTENSIONS = {'pdf'}

# appa = Flask(__name__)
# appa.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# appa.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/pdfs-3', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
        
#         # verifique se a solicitacao de postagem tem a parte do arquivo
#         if 'file' not in request.files:
#             flash('Nao tem a parte do arquivo')
#             return redirect(request.url)
#         file = request.files['file']
        
#         # Se o usuario nao selecionar um arquivo, o navegador envia um
#         # arquivo vazio sem um nome de arquivo.
        
#         if file.filename == '':
#             flash('Nenhum arquivo selecionado')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('download_file', name=filename))
#     return '''
#     <!doctype html>
#     <html>
#     <head>
#         <title>Upload File</title>
#     </head>
#     <body>
#         <h1>File Upload</h1>
#         <form method="POST" action="" enctype="multipart/form-data">
#         <p><input type="file" name="file"></p>
#         <p><input type="submit" value="Submit"></p>
#         </form>
#     </body>
#     </html>
#         '''
    
    
# @app.route('/uploads/<name>')
# def download_file(name):
#     return send_from_directory(app.config["UPLOAD_FOLDER"], name)
if __name__ == '__main__':
    app.run(debug=True)