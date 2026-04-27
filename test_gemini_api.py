import os
import sys

from dotenv import load_dotenv
import google.generativeai as genai


def main() -> int:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        print("ERRO: defina GOOGLE_API_KEY no arquivo .env.")
        print("Exemplo no arquivo .env.example")
        return 1

    genai.configure(api_key=api_key)

    try:
        model_names = []
        for model in genai.list_models():
            if "generateContent" in model.supported_generation_methods:
                model_names.append(model.name)

        if not model_names:
            print("ERRO: a API respondeu, mas nao ha modelos com generateContent.")
            return 1

        selected = (
            "models/gemini-1.5-pro"
            if "models/gemini-1.5-pro" in model_names
            else model_names[0]
        )

        model = genai.GenerativeModel(selected)
        response = model.generate_content("Responda com apenas: API OK")

        print("Conexao com API: OK")
        print(f"Modelo usado: {selected}")
        print(f"Resposta da IA: {response.text.strip()}")
        return 0
    except Exception as exc:
        print(f"ERRO ao conectar na API: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
