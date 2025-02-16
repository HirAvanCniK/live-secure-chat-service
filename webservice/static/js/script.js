let ws = undefined;
const chatContainer = document.querySelector('.chat-container');
const chatBox = document.getElementById('chat-box');
const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const hostname = window.location.hostname;

chatBox.scrollTop = chatBox.scrollHeight;

const connect = (btn, port) => {
    ws = new WebSocket(`ws://${hostname}:${port}`);
    ws.onopen = function(event) {
        console.log("WebSocket connection was successfully established");
        chatContainer.style.display = 'block';
        btn.style.display = 'none';

        ws.onmessage = function(event) {
            const message = event.data;
            const messageElement = document.createElement('div');
            messageElement.textContent = message;
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight;
        };

        ws.onerror = function(error) {
            console.error("WebSocket error:", error);
        };

        ws.onclose = function(event) {
            console.log("WebSocket connection closed:", event);
            chatContainer.style.display = 'none';
            btn.style.display = 'block';
        };
    }
}

sendButton.addEventListener('click', function() {
    if (!ws || ws.readyState !== WebSocket.OPEN) {
        console.error("WebSocket is not connected.");
        return;
    }
    const message = messageInput.value;
    if (message) {
        ws.send(message);
        messageInput.value = '';
    }
});

messageInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendButton.click();
    }
});

const checkbox = document.getElementById('checkbox');

const listOfElementsToChange = [document.body, chatContainer, chatBox, messageInput, document.querySelector(".input-container")];

const currentTheme = localStorage.getItem('theme');
if (currentTheme) {
    listOfElementsToChange.forEach((element) => {
        element.classList.add(currentTheme);
    });
    if (currentTheme != 'light-mode') {
        checkbox.checked = true;
    }
}

checkbox.addEventListener('change', function() {
    if (this.checked) {
        listOfElementsToChange.forEach((element) => {
            element.classList.add('dark-mode');
        });
        localStorage.setItem('theme', 'dark-mode');
    } else {
        listOfElementsToChange.forEach((element) => {
            element.classList.remove('dark-mode');
        });
        localStorage.setItem('theme', 'light-mode');
    }
});