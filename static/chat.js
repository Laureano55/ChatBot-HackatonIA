document.addEventListener("DOMContentLoaded", function() {
    function sendMessage() {
        var message = document.getElementById("message").value;
        
        var messagesContainer = document.getElementById("messages");
        var userMessageContainer = document.createElement("div");
        userMessageContainer.textContent = message;
        userMessageContainer.style.marginTop = "10px";
        userMessageContainer.classList.add("user-message");
        messagesContainer.appendChild(userMessageContainer);
        
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        document.getElementById("message").value = "";

        fetch("/send_message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (response.status === 429) {
                throw new Error("Demasiadas solicitudes. Por favor, vaya más despacio.");
            }
            return response.json();
        })
        .then(data => {
            var htmlContent = marked(data.messages[data.messages.length - 1]);
        
            var aiMessageContainer = document.createElement("div");
            aiMessageContainer.innerHTML = htmlContent;
            aiMessageContainer.style.marginTop = "10px";
            aiMessageContainer.classList.add("ai-message");
            messagesContainer.appendChild(aiMessageContainer);
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(error => {
            var errorMessageContainer = document.createElement("div");
            errorMessageContainer.textContent = error.message;
            errorMessageContainer.style.color = "red";
            errorMessageContainer.style.marginTop = "10px";
            errorMessageContainer.classList.add("ai-message");
            messagesContainer.appendChild(errorMessageContainer);
            
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        });
    }

    document.getElementById("sendButton").addEventListener("click", sendMessage);

    document.getElementById("message").addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});