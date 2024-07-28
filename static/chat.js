document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("sendButton").addEventListener("click", function() {
        var message = document.getElementById("message").value;
        fetch("/send_message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            var messagesContainer = document.getElementById("messages");
            messagesContainer.innerHTML = "";
            data.messages.forEach(function(msg) {
                var messageContainer = document.createElement("div");
                messageContainer.textContent = msg;
                messagesContainer.appendChild(messageContainer);
            });
            document.getElementById("message").value = ""; // Clear the input field
        });
    });
});