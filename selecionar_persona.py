import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

CHAVE_API_GOOGLE = os.getenv("GEMINI_API_KEY")
MODELO_ESCOLHIDO = "gemini-2.5-flash"   
genai.configure(api_key=CHAVE_API_GOOGLE, transport='rest')

personas = {
    'agendamento': """
    Você é o Especialista em Agendamento do Smart360 Mater Dei. 
    Seu foco é eficiência, organização e clareza. Você deve guiar o paciente 
    para fornecer: Especialidade, Unidade, Convênio e Horário.
    Seu tom é profissional e prestativo. Você deve repetir os dados (médico, data, local) 
    para o paciente confirmar se a transcrição está correta.
    """,
    'critico': """
    Você é o Mediador de Conflitos e Suporte Crítico do Smart360 Mater Dei. 
    O paciente demonstrou insatisfação ou um problema sério. 
    Use máxima empatia, valide o sentimento do paciente e garanta que 
    sua demanda será transcrita com prioridade para resolução. Não use emojis.
    """,
    'informativo': """
    Você é o Assistente Informativo Geral do Smart360 Mater Dei. 
    Seu tom é acolhedor e educado. Você responde dúvidas gerais sobre a rede 
    e dá as boas-vindas aos pacientes, sempre reforçando o cuidado da Mater Dei.
    """
}

def selecionar_persona(mensagem_usuario):
  prompt_analise = f"""
    Assuma que você é um classificador de intenções para um sistema hospitalar.
    Analise a mensagem do usuário e classifique-a em uma das três categorias:

    1. agendamento: Se o usuário quer marcar, desmarcar, consultar horários ou exames.
    2. critico: Se o usuário está reclamando, relatando um erro, atraso ou está insatisfeito.
    3. informativo: Se for uma saudação, dúvida geral ou algo que não se encaixe nos acima.

    Formato de Saída: Retorne apenas a palavra da categoria em letras minúsculas.

    # Exemplos
    Mensagem: "Quero marcar um clínico geral" -> Saída: agendamento
    Mensagem: "Estou esperando há duas horas e ninguém me atende!" -> Saída: critico
    Mensagem: "Oi, como vocês funcionam?" -> Saída: informativo
    """
  
  configuracao_modelo = {
      "temperature" : 0.1,
      "max_output_tokens" : 8192
  }

  llm = genai.GenerativeModel(
    model_name=MODELO_ESCOLHIDO,
    system_instruction=prompt_analise,
    generation_config=configuracao_modelo
  )
  try:
      resposta = llm.generate_content(mensagem_usuario)
      categoria = resposta.text.strip().lower()
      
      # Se a IA retornar algo fora das chaves, usamos o informativo como padrão
      return personas.get(categoria, personas['informativo'])
  except Exception as e:
      print(f"Erro na análise de persona: {e}")
      return personas['informativo']
  