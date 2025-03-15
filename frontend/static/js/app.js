const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.querySelector('button');

function disableInput(disabled = true) {
    userInput.disabled = disabled;
    sendButton.disabled = disabled;
}

function addLoadingMessage() {
    const loadingDiv = document.createElement('div');
    loadingDiv.classList.add('message', 'ai-message', 'loading');
    loadingDiv.textContent = 'Chi is thinking...';
    chatMessages.appendChild(loadingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return loadingDiv;
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.classList.add('error-message');
    errorDiv.textContent = message;
    chatMessages.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 3000);
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) {
        showError('Please enter a message');
        return;
    }

    disableInput(true);
    // Add user message to chat
    addMessage(message, 'user');
    userInput.value = '';
    
    const loadingMessage = addLoadingMessage();

    try {
        const response = await fetch('http://localhost:8000/api/conversations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({ user_message: message })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => null);
            console.error('Response error:', response.status, errorData);
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        loadingMessage.remove();
        // Add AI response to chat
        addMessage(data.ai_response, 'ai');
    } catch (error) {
        console.error('Error:', error);
        loadingMessage.remove();
        addMessage('Sorry, something went wrong.', 'ai');
    } finally {
        disableInput(false);
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Allow sending message with Enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Load previous conversations on page load
async function loadConversations() {
    try {
        const response = await fetch('http://localhost:8000/api/conversations/');
        const conversations = await response.json();
        
        conversations.forEach(convo => {
            addMessage(convo.user_message, 'user');
            addMessage(convo.ai_response, 'ai');
        });
    } catch (error) {
        console.error('Error loading conversations:', error);
    }
}

loadConversations();
