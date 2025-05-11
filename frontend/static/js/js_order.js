async function enviarPagamento(event) {
    event.preventDefault();
    
    const formaPagamento = document.getElementById('forma_pagamento').value;

    const user_id = getUserId(); 

    fetch(`http://localhost:8003/order_pay/${user_id}`, {
        method: "POST",  // ou GET se for só consulta
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            forma_pagamento: formaPagamento
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Erro no pagamento");
        }
        return response.json();
    })
    .then(data => {
        alert("Pagamento realizado com sucesso!");
        console.log(data);
        window.location.reload();  // Atualiza a página
    })
    .catch(error => {
        alert("Erro ao processar o pagamento.");
        console.error(error);
    });
}


// Função para obter o user_id, que você pode personalizar conforme a sua aplicação
function getUserId() {
    // Exemplo: pegar o user_id do localStorage ou de uma variável global
    return localStorage.getItem('user_id');
}