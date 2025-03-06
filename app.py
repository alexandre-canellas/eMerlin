from flask import Flask, request, render_template
from openai import OpenAI
from dotenv import load_dotenv
import os

from model.utils import allowed_file, read_uploaded_file, classify_and_answer

app = Flask(__name__)

load_dotenv()

# Set up OpenAI API key
client = OpenAI(
    api_key=os.environ["API_KEY"]
)

# Definição do caminho dos arquivos de upload e tipos permitidos de arquivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###############################         INICIALIZAÇÃO DO APP        ########################################

@app.route('/')
def home():
    return render_template("home.html"), 200

# Rotina de upload via seleção de arquivos txt ou pdf
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file.filename == '':
        error_text = "Nenhum arquivo selecionado"
        return render_template("error.html", error_text=error_text)
    
    if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        user_text = read_uploaded_file(filename)

        classification, answer = classify_and_answer(client, user_text)

        return render_template("answer.html", classification=classification, answer=answer)

    error_text = "Parece que o arquivo selecionado não tem o formato permitido (.txt | .pdf)"
    return render_template("error.html", error_text=error_text)

# Rotina de upload via caixa de texto
@app.route('/upload_text', methods=['POST'])
def upload_file_box():
    
    user_text = request.form['textBox']

    try:
        classification, answer = classify_and_answer(client, user_text)

        return render_template("answer.html", classification=classification, answer=answer)
    
    except Exception as e:
        error_text = "Parece que o texto não foi processado corretamente"
        return render_template("error.html", error_text=error_text)

if __name__ == '__main__':
    app.run(debug=True)