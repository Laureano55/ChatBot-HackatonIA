document.addEventListener("DOMContentLoaded", function() {
    function sendMessage() {
        var message = document.getElementById("message").value;
        
        // Display the user's message immediately
        var messagesContainer = document.getElementById("messages");
        var userMessageContainer = document.createElement("div");
        userMessageContainer.textContent = message;
        messagesContainer.appendChild(userMessageContainer);
        
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
        .then(response => response.json())
        .then(data => {
            // Display the AI's response
            var aiMessageContainer = document.createElement("div");
            aiMessageContainer.textContent = data.messages[data.messages.length - 1];
            messagesContainer.appendChild(aiMessageContainer);
        });
    }

    document.getElementById("sendButton").addEventListener("click", sendMessage);

    document.getElementById("message").addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });
});