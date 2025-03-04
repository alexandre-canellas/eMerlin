from flask import Flask, request, send_from_directory, render_template
import os

app = Flask(__name__)

# Definição do caminho dos arquivos de upload e tipos permitidos de arquivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template("home.html"), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']

    if file.filename == '':
        return 'Nenhum arquivo selecionado.'
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return 'Arquivo carregado com sucesso!'

    return 'Tipo de arquivo não permitido!'

if __name__ == '__main__':
    app.run(debug=True)