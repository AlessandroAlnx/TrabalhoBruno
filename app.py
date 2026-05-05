import os
import sys
import psycopg2
from psycopg2 import sql
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgress")
DB_PASSWORD = os.getenv("DB_PASSWORD", "9375")
DB_NAME = os.getenv("DB_NAME", "Trabalho.bruno")


def get_db_connection():
    """Retorna uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return conn
    except Exception as e:
        print(f"ERRO ao conectar ao banco: {e}")
        return None


def criar_tabelas():
    """Cria as tabelas necessárias se não existirem."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                senha VARCHAR(100) NOT NULL
            )
        """)
        
        # Tabela de códigos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS codigos (
                id_codigo SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL,
                codigo TEXT NOT NULL,
                linguagem VARCHAR(20),
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
            )
        """)
        
        # Tabela de análises
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analises (
                id SERIAL PRIMARY KEY,
                codigo_id INTEGER NOT NULL,
                erro TEXT,
                explicacao TEXT,
                codigo_corrigido TEXT,
                nivel_severidade VARCHAR(20),
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (codigo_id) REFERENCES codigos(id_codigo)
            )
        """)
        
        # Tabela de logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id SERIAL PRIMARY KEY,
                usuario_id INTEGER NOT NULL,
                acao VARCHAR(100),
                descricao TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
            )
        """)
        
        conn.commit()
        cursor.close()
        print("✓ Tabelas criadas com sucesso!")
        return True
    except Exception as e:
        print(f"ERRO ao criar tabelas: {e}")
        return False
    finally:
        conn.close()


def criar_usuario(nome, email, senha):
    """Cria um novo usuário no banco de dados."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s) RETURNING id_usuario",
            (nome, email, senha)
        )
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return user_id
    except psycopg2.IntegrityError:
        print(f"ERRO: Email {email} já existe!")
        conn.rollback()
        return None
    except Exception as e:
        print(f"ERRO ao criar usuário: {e}")
        return None
    finally:
        conn.close()


def login(email, senha):
    """Verifica se o usuário existe e a senha está correta."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, senha FROM usuarios WHERE email = %s",
            (email,)
        )
        resultado = cursor.fetchone()
        cursor.close()
        
        if resultado and resultado[1] == senha:
            return True
        return False
    except Exception as e:
        print(f"ERRO ao fazer login: {e}")
        return False
    finally:
        conn.close()


def inserir_codigo(usuario_id, codigo, linguagem="python"):
    """Insere um código no banco de dados."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO codigos (usuario_id, codigo, linguagem) VALUES (%s, %s, %s) RETURNING id_codigo",
            (usuario_id, codigo, linguagem)
        )
        codigo_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return codigo_id
    except Exception as e:
        print(f"ERRO ao inserir código: {e}")
        return None
    finally:
        conn.close()


def inserir_analise(codigo_id, erro, explicacao, codigo_corrigido, nivel_severidade):
    """Insere uma análise de código no banco de dados."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO analises 
               (codigo_id, erro, explicacao, codigo_corrigido, nivel_severidade) 
               VALUES (%s, %s, %s, %s, %s) RETURNING id""",
            (codigo_id, erro, explicacao, codigo_corrigido, nivel_severidade)
        )
        analise_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return analise_id
    except Exception as e:
        print(f"ERRO ao inserir análise: {e}")
        return None
    finally:
        conn.close()


def registrar_log(usuario_id, acao, descricao):
    """Registra uma ação do usuário no log."""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (usuario_id, acao, descricao) VALUES (%s, %s, %s)",
            (usuario_id, acao, descricao)
        )
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"ERRO ao registrar log: {e}")
        return False
    finally:
        conn.close()


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
