document.addEventListener('DOMContentLoaded', function () {
    const chatContainer = document.querySelector('.chat-container');
    const chatWindow = document.getElementById('chat-window');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const minimizeButton = document.querySelector('.minimize-button');

    // Chat toggle setup
    const toggleButton = document.createElement('div');
    toggleButton.className = 'chat-toggle';
    toggleButton.innerHTML = '💬';
    document.body.appendChild(toggleButton);

    // Event Listeners
    minimizeButton.addEventListener('click', (event) => {
        event.preventDefault();
        chatContainer.style.display = 'none';
        toggleButton.style.display = 'flex';
    });

    toggleButton.addEventListener('click', (event) => {
        event.preventDefault();
        chatContainer.style.display = 'block';
        toggleButton.style.display = 'none';
    });

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendMessage();
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessageToChat('User', message);

            fetch("https://e541-104-205-149-202.ngrok-free.app/webhooks/rest/webhook", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
                body: JSON.stringify({ sender: 'user', message }),
            })
            .then(response => response.json())
            .then(data => {
                console.log('Rasa Response:', data); // Debugging log
                
                if (data && data.length > 0) {
                    data.forEach(response => {
                        // Handle text message
                        if (response.text) {
                            addMessageToChat('Goodie-Bot', renderMarkdown(response.text));
                        }
                        
                        // Handle button template attachments
                        if (response.attachment && response.attachment.payload) {
                            const payload = response.attachment.payload;
                            if (payload.template_type === 'button' && payload.buttons) {
                                const buttonContainer = document.createElement('div');
                                buttonContainer.className = 'button-container';
                                
                                payload.buttons.forEach(button => {
                                    if (button.type === 'web_url') {
                                        const buttonElement = createButtonLink(button);
                                        buttonContainer.appendChild(buttonElement);
                                    }
                                });
                                
                                chatWindow.appendChild(buttonContainer);
                                chatWindow.scrollTop = chatWindow.scrollHeight;
                            }
                        }
                    });
                } else {
                    addMessageToChat('Goodie-Bot', "I didn't understand that. Can you rephrase?");
                }
            })
            .catch(error => {
                console.error('Error:', error);
                addMessageToChat('Goodie-Bot', 'Connection issue. Try again later.');
            });

            userInput.value = '';
        }
    }

    function createButtonLink(button) {
        const buttonElement = document.createElement('a');
        buttonElement.className = 'dynamic-button';
        buttonElement.href = button.url;
        buttonElement.target = '_blank';
        buttonElement.textContent = button.title;
        
        // Add PDF icon if it's a PDF link
        if (button.url.toLowerCase().endsWith('.pdf')) {
            buttonElement.innerHTML = `📄 ${button.title}`;
        }
        
        return buttonElement;
    }

    function renderMarkdown(text) {
        // Handle links first
        text = text.replace(/\[([^\]]+)\]\(([^\)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

        // Handle bold text
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Handle line breaks
        text = text.replace(/\n/g, '<br>');
        
        return text;
    }

    function addMessageToChat(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender.toLowerCase().replace(' ', '-'));
        const contentContainer = document.createElement('div');
        contentContainer.className = 'message-content';
        contentContainer.innerHTML = `<strong>${sender}:</strong> ${message}`;

        messageElement.appendChild(contentContainer);
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Initial greeting
    function addGreetingWithTopics() {
        addMessageToChat('Goodie-Bot', 'Welcome to our fake website. My name is Goodie, and I am your Academic Assistant! Please select a topic below:');

        const topicsContainer = document.createElement('div');
        topicsContainer.classList.add('topics-container');

        const topics = ['Programs', 'Admissions', 'Fees'];
        topics.forEach(topic => {
            const button = document.createElement('button');
            button.className = 'topic-button';
            button.innerText = topic;
            button.addEventListener('click', () => handleTopicSelection(topic));
            topicsContainer.appendChild(button);
        });

        chatWindow.appendChild(topicsContainer);
    }

    function handleTopicSelection(topic) {
        addMessageToChat('User', topic);

        fetch("https://e541-104-205-149-202.ngrok-free.app/webhooks/rest/webhook", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify({ sender: 'user', message: topic }),
        })
        .then(response => response.json())
        .then(data => handleRasaResponse(data))
        .catch(error => {
            console.error('Error:', error);
            addMessageToChat('Goodie-Bot', 'Connection issue. Try again later.');
        });
    }

    function handleRasaResponse(data) {
        if (data && data.length > 0) {
            data.forEach(response => {
                if (response.text) {
                    addMessageToChat('Goodie-Bot', renderMarkdown(response.text));
                }
                if (response.attachment && response.attachment.payload) {
                    handleButtonPayload(response.attachment.payload);
                }
            });
        } else {
            addMessageToChat('Goodie-Bot', "I didn't understand that. Can you rephrase?");
        }
    }

    function handleButtonPayload(payload) {
        if (payload.template_type === 'button' && payload.buttons) {
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'button-container';
            
            payload.buttons.forEach(button => {
                if (button.type === 'web_url') {
                    const buttonElement = createButtonLink(button);
                    buttonContainer.appendChild(buttonElement);
                }
            });
            
            chatWindow.appendChild(buttonContainer);
            chatWindow.scrollTop = chatWindow.scrollHeight;
        }
    }

    // Initialize the chatbot
    addGreetingWithTopics();
});
