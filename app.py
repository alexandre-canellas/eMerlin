from flask import Flask, request, render_template
from openai import OpenAI
import pdfplumber
import os

app = Flask(__name__)

# Set up OpenAI API key
client = OpenAI(
  api_key="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"
)

# Definição do caminho dos arquivos de upload e tipos permitidos de arquivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_uploaded_file(filename):
    
    if filename.endswith('.txt'):
        
        with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        
    with pdfplumber.open(filename) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        
        return text

###############################         INICIALIZAÇÃO DO APP        ########################################

@app.route('/')
def home():
    return render_template("home.html"), 200

# Rotina de upload via seleção de arquivos txt ou pdf
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file.filename == '':
        return 'Nenhum arquivo selecionado.'
    
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        user_text = read_uploaded_file(filename)

        return user_text

    return 'Tipo de arquivo não permitido!'

# Rotina de upload via caixa de texto
@app.route('/upload_text', methods=['POST'])
def upload_file_box():
    
    user_text = request.form['textBox']

    try:
        completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"Classifique o texto a seguir conforme a necessidade de resposta (ham): \n\n{user_text}\n\n Responda com 'NECESSARIO' ou 'DESNECESSARIO'.",
                    },
                ]
                # max_tokens=10,
                # temperature=0.1,
                # n=1,
                # stop=None,
            )

        # Extract the classification result from the response
        classification = completion.choices[0].message.content

        # Return a message based on the classification result
        if classification == 'NECESSARIO':
            result_message = "PRODUTIVO"
            return f"Classificação: {result_message} \n\nSegue abaixo a resposta sugerida:"
        else:
            result_message = "IMPRODUTIVO"
            return f"Classificação: {result_message} \n\nPortanto, não há necessidade de resposta!"
    
    except Exception as e:
        return f'Erro no upload do texto: {e}'

if __name__ == '__main__':
    app.run(debug=True)