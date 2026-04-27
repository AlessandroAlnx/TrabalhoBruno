import os
import sys

from dotenv import load_dotenv
import google.generativeai as genai


def create_chat() -> tuple[object, str]:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Defina GOOGLE_API_KEY no arquivo .env")

    genai.configure(api_key=api_key)

    models = [
        m.name
        for m in genai.list_models()
        if "generateContent" in m.supported_generation_methods
    ]
    if not models:
        raise RuntimeError("Nenhum modelo com generateContent foi encontrado.")

    preferred = "models/gemini-1.5-pro"
    selected = preferred if preferred in models else models[0]
    model = genai.GenerativeModel(selected)
    chat = model.start_chat(history=[])
    return chat, selected


def main() -> int:
    try:
        chat, model_name = create_chat()
    except Exception as exc:
        print(f"ERRO: {exc}")
        print("Dica: copie .env.example para .env e preencha sua chave.")
        return 1

    print("Aplicacao iniciada com sucesso.")
    print(f"Modelo: {model_name}")
    print("Digite sua pergunta. Use 'sair' para encerrar.")

    # Contexto fixo para respostas em portugues.
    chat.send_message("Responda sempre em portugues do Brasil.")

    while True:
        pergunta = input("Voce: ").strip()
        if pergunta.lower() in {"sair", "exit", "quit"}:
            print("Encerrando.")
            break
        if not pergunta:
            continue

        try:
            resposta = chat.send_message(pergunta)
            print(f"IA: {resposta.text.strip()}")
        except Exception as exc:
            print(f"ERRO ao consultar a IA: {exc}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
