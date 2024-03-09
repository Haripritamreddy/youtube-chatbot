# YouTube Chatbot

This project is a chatbot that can fetch YouTube transcripts and generate responses based on the video content using OpenAI's language model. It consists of two components: a Flask server and a Chrome browser extension.

# TODO

- [ ] Implement a user interface for `main.py` to improve the user experience and make it more interactive.

### What is happening?

## Flask Server

The Flask server is responsible for fetching YouTube transcripts, embedding them using Google's Generative AI Embeddings, and retrieving relevant parts based on the user's query using Chroma vector store. For other embeddings refer Lanchain Docs.

The server will be available at `http://127.0.0.1:5000`.

## Chrome Extension

The Chrome extension provides a user interface for interacting with the chatbot. It retrieves the YouTube video ID from the current tab, sends the user's message to the Flask server, and displays the generated response.

### Installation

1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable "Developer mode" by toggling the switch in the top-right corner.
3. Click "Load unpacked" and select the directory containing the extension files (`manifest.json`, `popup.html`, `popup.js`,  `popup.css` and `server.py`).

### Extension Usage

1. Navigate to a YouTube video.
2. Click the extension icon in the Chrome toolbar.
3. Type your message in the input field and press Enter or click the send button.
4. The chatbot will fetch the relevant part of the transcript and generate a response based on your message.

## Standalone CLI Chat

The `main.py` script provides a command-line interface for chatting with YouTube videos. It uses the same functionality as the Flask server and Chrome extension but runs in a standalone environment. I does not require a flask server or Chrome extension to be used.

## Working

1.Load the chrome extension or use main.py.
2.Install required dependencies.
3. Enter a YouTube URL when prompted.
4. Type your query, and the script will fetch the relevant part of the transcript, generate a response, and display it.
5. To exit, type `exit`.

## Note

- Make sure to replace `YOUR_API_KEY` in `main.py` with your actual  API key.
- The Chrome extension uses the Naga.ai API for generating responses. You may need to adjust the API key and URL in `popup.js` based on your setup.
- Since this is OpenAI compatable you can use almost any model you run. For embeddings also it's the same(Please refer to langchain docs.)