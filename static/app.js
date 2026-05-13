const form = document.getElementById("pergunta-form");
const perguntaInput = document.getElementById("pergunta");
const respostaEl = document.getElementById("resposta");
const statusEl = document.getElementById("status");
const btnEnviar = document.getElementById("btn-enviar");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const pergunta = perguntaInput.value.trim();
  if (!pergunta) {
    statusEl.textContent = "Digite uma pergunta antes de enviar.";
    statusEl.classList.add("error");
    return;
  }

  statusEl.textContent = "Consultando a IA...";
  statusEl.classList.remove("error");
  respostaEl.textContent = "";
  btnEnviar.disabled = true;

  try {
    const response = await fetch("/api/perguntar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ pergunta }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.erro || "Falha na requisicao.");
    }

    respostaEl.textContent = data.resposta || "Sem conteudo retornado.";
    statusEl.textContent = "Resposta recebida com sucesso.";
  } catch (error) {
    statusEl.textContent = "Nao foi possivel obter resposta agora.";
    statusEl.classList.add("error");
    respostaEl.textContent = error.message;
  } finally {
    btnEnviar.disabled = false;
  }
});
