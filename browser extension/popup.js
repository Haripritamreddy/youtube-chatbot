document.addEventListener('DOMContentLoaded', function () {
    const chatOutput = document.getElementById('chat-output');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    sendBtn.addEventListener('click', sendMessage);

    userInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });

    async function sendMessage() {
        const userMessage = userInput.value;
        const videoId = await getYouTubeVideoId();

        if (!videoId) {
            console.error('Video ID not found.');
            return;
        }

        const relevantContent = await getRelevantContent(videoId, userMessage);
        appendMessage(userMessage, 'user-message');
        getOpenAIResponse(userMessage, relevantContent);
        userInput.value = '';
    }

    async function getYouTubeVideoId() {
        return new Promise((resolve, reject) => {
            chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
                const url = tabs[0].url;
                const urlParams = new URLSearchParams(url.split('?')[1]);
                const videoId = urlParams.get('v');

                if (videoId) {
                    resolve(videoId);
                } else {
                    const pathSegments = new URL(url).pathname.split('/');
                    const index = pathSegments.indexOf('watch');

                    if (index !== -1 && index + 1 < pathSegments.length) {
                        resolve(pathSegments[index + 1]);
                    } else {
                        reject('Unable to retrieve the YouTube video ID.');
                    }
                }
            });
        });
    }

    function appendMessage(message, messageClass) {
        const messageElement = document.createElement('div');
      
        if (messageClass === 'user-message') {
          messageElement.classList.add('message', 'user-message');
          const userBubble = document.createElement('div');
          userBubble.textContent = message;
          userBubble.classList.add('user-bubble');
          messageElement.appendChild(userBubble);
        } else if (messageClass === 'bot-message') {
          messageElement.classList.add('message', 'bot-message');
          const botBubble = document.createElement('div');
          botBubble.textContent = message;
          botBubble.classList.add('bot-bubble');
          messageElement.appendChild(botBubble);
        }
      
        chatOutput.appendChild(messageElement);
        chatOutput.scrollTop = chatOutput.scrollHeight;
    }

    async function getRelevantContent(videoId, userMessage) {
        const apiUrl = 'http://127.0.0.1:5000/get_relevant';

        try {
            const response = await axios.get(apiUrl, {
                params: {
                    video_id: videoId,
                    user_message: userMessage,
                },
            });

            const relevantContentObject = response.data;
            const relevantContentText = relevantContentObject.relevant_content || '';
            console.log('Relevant Content:', relevantContentText);
            return relevantContentText;
        } catch (error) {
            console.error('Error fetching relevant content:', error.message);
            throw error;
        }
    }

    async function getOpenAIResponse(userMessage, relevantContent) {
        const apiKey = 'YOUR_API_KEY';
        const apiUrl = 'https://api.naga.ac/v1/chat/completions';

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({
                    model: 'gpt-3.5-turbo',
                    messages: [
                        { role: 'system', content: 'You are a helpful assistant. Answer questions based on the Relevant context. Even though other things may exist only naser based on the context provided.' },
                        { role: 'user', content: userMessage + "Relevant content: " + relevantContent }
                    ]
                })
            });

            const data = await response.json();
            console.log('OpenAI Response:', data);
            const choices = data.choices || [];

            if (choices.length > 0) {
                const botResponse = choices[0].message.content.trim();
                appendMessage(botResponse, 'bot-message');
            } else {
                console.error('No choices in the OpenAI response.');
            }
        } catch (error) {
            console.error('Error getting OpenAI response:', error);
        }
    }
});
