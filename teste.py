from app import criar_usuario, login, inserir_codigo, inserir_analise, registrar_log

# =========================
# CRIA USUÁRIO
# =========================
user_id = criar_usuario("João", "joao@email.com", "1234")
print("User ID:", user_id)

# =========================
# LOGIN (teste)
# =========================
logado = login("joao@email.com", "1234")
print("Login OK:", logado)

# =========================
# INSERE CÓDIGO
# =========================
codigo_id = inserir_codigo(user_id, "print('hello world')")
print("Codigo ID:", codigo_id)

# =========================
# INSERE ANÁLISE
# =========================
inserir_analise(
    codigo_id,
    erro=None,
    explicacao="Código correto",
    codigo_corrigido="print('hello world')",
    nivel_severidade="baixo"
)

# =========================
# LOG DO SISTEMA
# =========================
registrar_log(user_id, "INSERT", "Inseriu código e análise")

print("Tudo executado com sucesso!")