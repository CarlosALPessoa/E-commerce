// Função para comprar o livro
    function buyBook(livroId) {
        const token = localStorage.getItem('access_token');
        const userId = localStorage.getItem('user_id'); // <- você precisa salvar o user_id após o login

        if (!token || !userId) {
            alert("Você precisa estar logado para realizar uma compra.");
            return;
        }

        const requestData = {
            book_id: livroId,
            user_id: userId
        };
    
        fetch('http://127.0.0.1:8003/sales/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}` // Passa o token de autenticação no cabeçalho
            },
            body: JSON.stringify(requestData) // Envia os dados no corpo da requisição
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw err });
            }
            return response.json();
        })
        .then(data => {
            alert("Adicionado ao carrinho!");
        })
        .catch(error => console.error('Erro ao realizar pagamento:', error));
    }

    function toggleDetails(livroId) {
        const details = document.getElementById('details-' + livroId);
        const button = details.previousElementSibling;
    
        const currentDisplay = window.getComputedStyle(details).display;
    
        if (currentDisplay === "none") {
            details.style.display = "block";
            button.textContent = "Ocultar Detalhes";
        } else {
            details.style.display = "none";
            button.textContent = "Mostrar Detalhes";
        }
    }