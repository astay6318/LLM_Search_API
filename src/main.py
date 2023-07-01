import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from dolly import load_llm_model
from datetime import datetime, timedelta
import documents
import concurrent.futures
import threading
import search

load_dotenv()
Cookie_VAL=os.getenv('COOKIE_VAL')

app = Flask(__name__)
llm_model = None
embeddings_done = False
embeddings_timestamp = None

EMBEDDINGS_FOLDER = '../faiss_index'
EMBEDDINGS_EXPIRY_DAYS = 7

@app.route('/api/search')
def handle_request():

    if not embeddings_done:
        return jsonify({'error': 'Embeddings are being done'}), 503
    
    if llm_model is None:
        return jsonify({'error': 'Model is still being loaded'}), 503

    query = request.args.get('query')
    return jsonify({'result': search.Similarity_Search_Using_Embeddings(query,Cookie_VAL,llm_model)})

@app.route('/')
def check():

    if not embeddings_done:
        return jsonify({'error': 'Embeddings are being done'}), 503
    if llm_model is None:
        return jsonify({'error': 'Model is still being loaded'}), 503

    return jsonify({'result': 'Good to Go! Start searching!'})

def start_app():
    app.run()


def initialize():
    global llm_model, embeddings_done,embeddings_timestamp

    # Check if embeddings exist and check the timestamp
    if documents.check_embeddings_exist(EMBEDDINGS_FOLDER):
        timestamp = documents.get_embeddings_timestamp(EMBEDDINGS_FOLDER)
        if timestamp is not None and (datetime.now() - timestamp) < timedelta(days=EMBEDDINGS_EXPIRY_DAYS):
            embeddings_done = True
            embeddings_timestamp = timestamp
            llm_model= load_llm_model()
            return

    documents.clear_embeddings(EMBEDDINGS_FOLDER)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        embeddings_future = executor.submit(documents.return_embeddings, Cookie_VAL)
        llm_model_future = executor.submit(load_llm_model)

        embeddings_done = embeddings_future.result()
        llm_model = llm_model_future.result()
    
    embeddings_timestamp = datetime.now()
    
if __name__ == '__main__':
    app_thread = threading.Thread(target=start_app)
    app_thread.start()

    initialize()
    app_thread.join()
