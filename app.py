from flask import Flask,render_template, request, Response
import google.generativeai as genai
from dotenv import load_dotenv
import os
from time import sleep
from helper import carrega, salva
from selecionar_persona import personas, selecionar_persona
from gerenciar_historico import remover_mensagens_mais_antigas
import uuid
from gerenciar_imagem import gerar_imagem_gemini
from pathlib import Path


load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
print(CHAVE_API_GOOGLE)
MODELO_ESCOLHIDO = "gemini-2.5-flash"   
genai.configure(api_key=CHAVE_API_GOOGLE, transport='rest')

app = Flask(__name__)
app.secret_key = 'alura'

contexto = carrega("dados/smart360.txt")

caminho_imagem_enviada = None
UPLOAD_FOLDER = "imagens_temporarias"

def criar_chatbot():
    personalidade = "neutro"

    prompt_do_sistema = f"""
    # OBJETIVO
    Você é o Smart360, assistente da Rede Mater Dei de Saúde. 
    Use o contexto abaixo para responder dúvidas e auxiliar no agendamento de consultas.
    Não responda perguntas fora do escopo de saúde e da clínica.

    # CONTEXTO
    {contexto}

    # REGRAS
    1. Se o paciente quiser marcar consulta, peça: Especialidade, Unidade, Convênio e Horário.
    2. Seja sempre ético e siga a LGPD.

    # Histórico
    Acesse sempre o históricio de mensagens, e recupere informações ditas anteriormente.
    """

    configuracao_modelo = {
        "temperature" : 0.1,
        "max_output_tokens" : 8192
    }

    llm = genai.GenerativeModel(
        model_name=MODELO_ESCOLHIDO,
        system_instruction=prompt_do_sistema,
        generation_config=configuracao_modelo
    )

    chatbot = llm.start_chat(history=[])

    return chatbot

chatbot = criar_chatbot()

def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    global caminho_imagem_enviada

    while True:
        try:
            #persona é selecionada dinamicamente baseada no que o usuário acabou de digitar.
            persona_texto = selecionar_persona(prompt) 
            
            mensagem_com_instrucao = f"""
            [INSTRUÇÃO DE ESTILO E PERSONA: {persona_texto}]
            
            Mensagem do Paciente: {prompt}
            """

            if caminho_imagem_enviada:
                arquivo_imagem = gerar_imagem_gemini(caminho_imagem_enviada)
                resposta = chatbot.send_message([arquivo_imagem, mensagem_com_instrucao])
                os.remove(caminho_imagem_enviada)
                caminho_imagem_enviada = None
            else:
                resposta = chatbot.send_message(mensagem_com_instrucao)

            # Mantém o histórico limpo para não estourar tokens
            if len(chatbot.history) > 10:
                chatbot.history = remover_mensagens_mais_antigas(chatbot.history)

            return resposta.text
        
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return f"Erro no Smart360: {erro}"
            sleep(1)


@app.route("/upload_imagem", methods=["POST"])
def upload_imagem():
    global caminho_imagem_enviada

    if "imagem" in request.files:
        imagem_enviada = request.files["imagem"]
        nome_arquivo = str(uuid.uuid4()) + os.path.splitext(imagem_enviada.filename)[1]
        caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
        imagem_enviada.save(caminho_arquivo)
        caminho_imagem_enviada = caminho_arquivo
        return "Imagem enviada com sucesso", 200
    return "Nenhum arquivo enviado", 400

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)
    return resposta

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)
