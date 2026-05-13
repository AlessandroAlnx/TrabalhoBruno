from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os

# Carrega variaveis do .env
load_dotenv()

# Captura chave da API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY nao encontrada. Configure no arquivo .env")

# Configuracao do modelo Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=api_key,
    temperature=0.7,
)

# Criacao do prompt
prompt = ChatPromptTemplate.from_template(
    """
    Voce e um especialista em tecnologia.

    Responda a seguinte pergunta:
    {pergunta}
    """
)

# Criacao da chain
chain = prompt | llm

# Entrada do usuario
pergunta_usuario = input("Digite sua pergunta: ")

# Execucao
resposta = chain.invoke({"pergunta": pergunta_usuario})

# Saida
print("\nResposta da IA:\n")
print(resposta.content)
