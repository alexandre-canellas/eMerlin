import pdfplumber

def read_uploaded_file(filename):
    # Retorna o conteúdo do arquivo após upload de acordo com sua extensão
    if filename.endswith('.txt'):
        
        with open(filename, 'r', encoding='utf-8') as file:
                return file.read()
        
    with pdfplumber.open(filename) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        
        return text
    
def allowed_file(filename, extensions):
    # Confere se o arquivo enviado é do tipo permitido
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

def classify_and_answer(client, user_text):
    # Faz uma chamada para openAI e classifica o texto
    # Em caso de classificação produtiva, retorna a sugestão de resposta também
    completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"Classifique o texto a seguir conforme a necessidade de resposta (ham): \n\n{user_text}\n\n Responda com 'NECESSARIO' ou 'DESNECESSARIO'. Em seguida, sugira uma resposta adequada ao texto.",
                    },
                ]
            )

    # Classificação e resposta sugerida
    classification = completion.choices[0].message.content.split(maxsplit=1)[0]
    suggested_answer = completion.choices[0].message.content.split(':',maxsplit=2)[1]

    # Retorna a classificação e reposta sugerida (quando couber resposta)
    if classification == 'NECESSARIO':
        return "PRODUTIVO", suggested_answer
    else:
        return "IMPRODUTIVO", "Não há necessidade de resposta!"