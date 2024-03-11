# YouTube Chatbot

This project features a chatbot designed to fetch YouTube transcripts and generate responses based on video content using OpenAI compatable API. It comprises two primary components: Embedding/Querying the transcript, Generating response based on relevant context.

# TODO

- [x] Implement a user interface for `main.py` to improve the user experience and make it more interactive.
- [ ] Update chat interface to enhance user interface and allow for multiple chats.

## Installation and Setup

```bash
pip install -r requirements.txt
```

## Usage

1. Use with Chrome extension on youtube page itself.
2. CLI chat with `main.py` .
3. Use web UI `ui.py`.


## Chrome Extension

The Chrome extension provides a user interface for interacting with the chatbot. 
### Follow these steps for installation:

1. Open Google Chrome and go to `chrome://extensions/`.
2. Enable "Developer mode" by toggling the switch in the top-right corner.
3. Click "Load unpacked" and select the directory containing the extension files (manifest.json, popup.html, popup.js, popup.css, and server.py).


### Flask Server

The Flask server is responsible for handling YouTube transcripts, embedding them with Google's Generative AI Embeddings, and retrieving relevant parts based on user queries using Chroma vector store. The server is accessible at `http://127.0.0.1:5000`.

To set up the Flask server:

```bash
python server.py
```


### Extension Usage
1. Run the Flask server using the provided instructions.
2. Navigate to a YouTube video.
3. Click the extension icon in the Chrome toolbar.
4. Input your message in the provided field and press Enter or click the send button.
5. The chatbot will fetch the relevant part of the transcript and generate a response based on your message.

### Standalone CLI Chat (main.py)
The `main.py` script provides a command-line interface for chatting with YouTube videos. It uses the same functionality as the Flask server and Chrome extension but runs in a standalone environment. No Flask server or Chrome extension is required.



### Web UI Usage

The web interface offers an interactive way to engage with the YouTube Chatbot. Follow these steps:

1. Run (`python ui.py`).
2. Open your web browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).
3. Enter a YouTube video URL.
4. Type your message in the provided input field and press Enter or click the send button.
5. The chatbot will fetch the relevant part of the transcript and generate a response based on your message.

## Important Notes

- Replace `YOUR_API_KEY` in `main.py` with your actual API key.
- The Chrome extension uses the Naga.ai API for generating responses. Adjust the API key and URL in `popup.js` based on your setup.
- This project is OpenAI-compatible, allowing you to use various language models and embeddings (refer to Langchain docs).
