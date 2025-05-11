async function login() {
  const username = prompt("Digite o usuário:");
  const password = prompt("Digite a senha:");

  const response = await fetch("http://localhost:3000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });

  if (response.ok) {
    const data = await response.json();
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("user_id", data.user_id);
    localStorage.setItem("username", data.username);
    localStorage.setItem("role", data.role); 
    alert("Login realizado com sucesso!");
    renderAuthButtons();
    updateWelcomeMessage();
    updateAdminLink();
  } else {
    alert("Falha no login");
  }
}

function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_id"); // Remover o user_id também ao fazer logout
  localStorage.removeItem("username");
  localStorage.removeItem("role"); 
  alert("Você saiu com sucesso.");
  renderAuthButtons(); // Atualiza a navbar sem recarregar
  updateWelcomeMessage();
  updateAdminLink();

  window.location.href = "/";
}

function updateWelcomeMessage() {
  const username = localStorage.getItem("username");
  const welcomeContainer = document.getElementById("welcome-msg");

  if (username && welcomeContainer) {
    welcomeContainer.textContent = `Bem-vindo, ${username}`;
  } else if (welcomeContainer) {
    welcomeContainer.textContent = ""; // limpa ao deslogar
  }
}

function renderAuthButtons() {
  const token = localStorage.getItem("access_token");
  const authContainer = document.getElementById("auth-buttons");

  authContainer.innerHTML = token
    ? `<button onclick="logout()">Sair</button>`
    : `<button onclick="login()">Entrar</button><button onclick="register()">Registrar</button>`;
}

function updateAdminLink(){
  const adminLink = document.getElementById("admin-link");
  const role = localStorage.getItem("role");

  if (role === "admin") {
    adminLink.style.display = "inline";
  } else {
    adminLink.style.display = "none";
  }
}

async function register(){
  const username = prompt("Digite um nome de usuário:");
  const password = prompt("Digite uma senha para sua conta:");

  const response = await fetch(
    "http://127.0.0.1:3000/register",{
      method: "POST",
      headers:{
        "Content-Type": "application/json"
      },
      body: JSON.stringify({username, password})
    });
  
    if(response.ok){
      alert("Registro realizado com sucesso! Faça login.")
    } else{
      const err = await response.json();
      alert("Erro ao registrar: "+err.message);
    }
}

// Executa ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
  renderAuthButtons();
  updateWelcomeMessage();
  updateAdminLink();
});

document.addEventListener("DOMContentLoaded", function() {
  const user_id = localStorage.getItem("user_id");

  if (user_id) {
    const carrinhoLink = document.getElementById("carrinho-link");
    carrinhoLink.href = `/carrinho?user_id=${user_id}`; // Atualiza o link do carrinho com o user_id
  } else {
    console.log("Usuário não autenticado, carrinho não configurado.");
  }
});


