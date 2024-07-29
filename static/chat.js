document.addEventListener("DOMContentLoaded", function() {
    function sendMessage() {
        var message = document.getElementById("message").value;
        
        // Display the user's message immediately
        var messagesContainer = document.getElementById("messages");
        var userMessageContainer = document.createElement("div");
        userMessageContainer.textContent = message;
        userMessageContainer.style.marginTop = "10px";
        userMessageContainer.classList.add("user-message");
        messagesContainer.appendChild(userMessageContainer);
        
        // Scroll to the bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Clear the input field
        document.getElementById("message").value = "";

        // Send the message to the server
        fetch("/send_message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => {
            if (response.status === 429) {
                throw new Error("Too many requests. Please try again later.");
            }
            return response.json();
        })
        .then(data => {
            // Parse the markdown response to HTML
            var htmlContent = marked(data.messages[data.messages.length - 1]);
        
            // Create a new div for the AI's message
            var aiMessageContainer = document.createElement("div");
            aiMessageContainer.innerHTML = htmlContent; // Use innerHTML to render the HTML content
            aiMessageContainer.style.marginTop = "10px";
            aiMessageContainer.classList.add("ai-message");
            messagesContainer.appendChild(aiMessageContainer);
            
            // Scroll to the bottom
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        })
        .catch(error => {
            // Display the error message in red
            var errorMessageContainer = document.createElement("div");
            errorMessageContainer.textContent = error.message;
            errorMessageContainer.style.color = "red";
            errorMessageContainer.style.marginTop = "10px";
            errorMessageContainer.classList.add("ai-message");
            messagesContainer.appendChild(errorMessageContainer);
            
            // Scroll to the bottom
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