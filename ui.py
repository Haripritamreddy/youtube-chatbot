import os
import datetime
from flask import Flask, render_template, request, redirect, session, url_for
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
import requests

app = Flask(__name__, static_folder='static')

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = input("Provide your Google API key here: ")

class Document:
    def __init__(self, page_content):
        self.page_content = page_content

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join(entry['text'] for entry in transcript)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"temp_{timestamp}.txt"
        new_file = True
        if 'file_name' in session:
            old_file_name = session['file_name']
            if os.path.exists(old_file_name):
                os.remove(old_file_name)
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(transcript_text)
        session['file_name'] = file_name
        return file_name, transcript_text.strip(), new_file
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None, "Transcript not found", False

def embed_and_query_chroma(query, file_name):
    loader = UnstructuredFileLoader(file_name)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma.from_documents(docs, embedding_function)
    relevant_part_docs = db.similarity_search(query)
    relevant_part = relevant_part_docs[0].page_content
    print(f"Relevant Part: {relevant_part}")
    return relevant_part

def generate_response(user_message, relevant_part):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer YOUR_API_KEY",
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Answe questions based on context."},
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": relevant_part},
            ],
            "temperature": 0.7,
        },
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        return f"Error {response.status_code}: {response.text}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        youtube_url = request.form['youtube_url']
        video_id = youtube_url.split('v=')[-1]
        file_name, full_transcript, new_file = get_youtube_transcript(video_id)
        if file_name:
            if new_file:
                session.pop('conversation', None)  # Clear old conversation if a new file was created
            return redirect(url_for('chatbot'))
    return render_template('index.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        user_message = request.form['user_message']
        file_name = session.get('file_name')
        relevant_part = embed_and_query_chroma(user_message, file_name)
        response = generate_response(user_message, relevant_part)
        conversation = session.get('conversation', [])
        conversation.append((user_message, response))
        session['conversation'] = conversation
        return render_template('chatbot.html', conversation=conversation)

    return render_template('chatbot.html', conversation=[])

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'
    app.run(debug=True)