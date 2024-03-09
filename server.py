from flask import Flask, request, jsonify
import os
import datetime
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'chrome-extension://gmajdbbaoocpiiblpalookooclfbfelc'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Adjust if needed
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Adjust if needed
    return response

@app.route('/get_relevant', methods=['GET'])
def get_relevant():
    video_id = request.args.get('video_id')
    user_message = request.args.get('user_message')

    if not video_id or not user_message:
        return jsonify({"error": "Both video_id and user_message are required"}), 400

    file_name, full_transcript = get_youtube_transcript(video_id)

    if file_name:
        try:
            relevant_part = embed_and_query_chroma(user_message, file_name)
            return jsonify({"relevant_content": relevant_part})
        finally:
            os.remove(file_name)
    else:
        return jsonify({"error": "Transcript not found"}), 404

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join(entry['text'] for entry in transcript)

        # Generate timestamp for unique file name
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"temp_{timestamp}.txt"

        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(transcript_text)

        return file_name, transcript_text.strip()
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return None, "Transcript not found"

def embed_and_query_chroma(query, file_name):
    loader = UnstructuredFileLoader(file_name)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma.from_documents(docs, embedding_function)
    docs = db.similarity_search(query)
    return docs[0].page_content

if __name__ == '__main__':
    app.run(debug=True)
