🧠 Smart360 — Rede Mater Dei de Saúde (Challenge 2025)
📋 Sobre o Projeto

O Smart360 é uma solução de inteligência artificial desenvolvida para a Rede Mater Dei de Saúde, com o objetivo de otimizar a jornada do paciente por meio de um atendimento mais preciso, eficiente e humanizado.

Nesta sprint, o foco está na definição da arquitetura inicial e no desenho da solução, estruturando as bases para um sistema escalável e orientado a dados.

A aplicação utiliza modelos de linguagem (LLMs) para garantir alta fidelidade na interpretação de demandas em voz e texto, superando desafios como:

- interferências sonoras
- variações linguísticas
- diversidade de sotaques

🚀 Funcionalidades (Sprint 2)

- Triagem e Identificação de Intenção
    Análise de sentimento para identificar se o paciente deseja realizar um agendamento ou registrar uma reclamação crítica.
- Personas Dinâmicas
    O chatbot adapta seu comportamento conforme o contexto:
        - Especialista em Agendamento
        - Mediador de Conflitos
        - Assistente Geral
- Correção de Contexto
Ajuste automático de transcrições para garantir fidelidade ao conteúdo original.
- Otimização de Texto
Remoção de redundâncias para melhorar a clareza e eficiência no processamento.
- Fluxo de Agendamento
    Coleta estruturada de informações como:
        - especialidade
        - unidade
        - convênio
        - horário
🛠️ Tecnologias Utilizadas
- Python 3.10+ — Desenvolvimento e análise de dados
- Flask — Framework web para prototipação
- Google Gemini API — Inteligência artificial generativa e análise de sentimentos
    
## 🔧 Como Rodar o Projeto Localmente

### 1. Clone o repositório
```bash
git clone https://github.com/YuitiNissi/smart360-chatbot.git
cd smart360-chatbot 
```
2. Crie e ative o ambiente virtual
```bash
python -m venv venv
```
Windows
```bash
venv\Scripts\activate
```
Mac/Linux
```bash
source venv/bin/activate
```
3. Instale as dependências
```bash
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente
Crie um arquivo .env na raiz do projeto:
```env
GEMINI_API_KEY=SUA_CHAVE_AQUI
```
5. Execute a aplicação
```bash
python app.py
```

📊 Planejamento e Gestão

O projeto segue a metodologia ágil com Kanban, garantindo:
- organização das tarefas
- visibilidade do progresso
- entregas contínuas

A arquitetura foi pensada para ser escalável, permitindo integração com:
- planilhas (Excel)
- sistemas ERP
- ferramentas de visualização de dados

🎯 Contexto Acadêmico

Este projeto é um entregável da Sprint 2 — Challenge FIAP & Rede Mater Dei de Saúde, com foco na aplicação prática de:
- inteligência artificial
- engenharia de dados
- arquitetura de sistemas