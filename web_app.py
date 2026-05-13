import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

app = Flask(__name__)


def build_chain() -> object:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY nao encontrada no arquivo .env")

    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest",
        google_api_key=api_key,
        temperature=0.6,
    )

    prompt = ChatPromptTemplate.from_template(
        """
        Voce e o assistente do site Copa 26 de ENG.
        Fale em portugues do Brasil, com resposta clara e amigavel.

        Pergunta do usuario:
        {pergunta}
        """
    )

    return prompt | llm


chain = build_chain()


@app.get("/")
def home() -> str:
    return render_template("index.html")


@app.post("/api/perguntar")
def perguntar() -> tuple[object, int] | object:
    payload = request.get_json(silent=True) or {}
    pergunta = str(payload.get("pergunta", "")).strip()

    if not pergunta:
        return jsonify({"erro": "Envie uma pergunta valida."}), 400

    try:
        resposta = chain.invoke({"pergunta": pergunta})
        conteudo = resposta.content

        if isinstance(conteudo, list):
            partes = [item.get("text", "") for item in conteudo if isinstance(item, dict)]
            texto = "\n".join(parte for parte in partes if parte).strip()
        else:
            texto = str(conteudo).strip()

        if not texto:
            texto = "Nao consegui gerar resposta agora. Tente novamente."

        return jsonify({"resposta": texto})
    except Exception as exc:
        return jsonify({"erro": f"Falha ao consultar IA: {exc}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
