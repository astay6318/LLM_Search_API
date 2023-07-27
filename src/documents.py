import html2text
import requests
from dotenv import load_dotenv
import os
import shutil
import glob
from datetime import datetime
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings, SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import ConfluenceLoader

# def extract_ids_from_links(links):
#     ids = []

#     for link in links:
#         if "/pages/" in link:
#             start_index = link.index("/pages/") + len("/pages/")
#             end_index = link.find("/", start_index)
#             id_value = link[start_index:end_index]
#             ids.append(id_value)

#     return ids

# def extract_content_from_html(html):
#     converter = html2text.HTML2Text()
#     converter.ignore_links = False 
#     plain_text = converter.handle(html)
#     return plain_text


# def fetchDocumentById(id, cookie):
#     url = f"https://simpl.atlassian.net/wiki/rest/api/content/{id}?expand=body.storage"
#     headers = {
#         "Cookie": cookie
#     }
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         plain_text=extract_content_from_html(dict(response.json())['body']['storage']['value'])
#         cleaned_text = ' '.join(plain_text.splitlines()).strip()
#         return  cleaned_text
#     else:
#         print(url)
#         return None

# def fetch_documents_content(ids, cookie):
#     documents = []
#     for id in ids:
#         html_content = fetchDocumentById(id, cookie)
#         if html_content:
#             text_content = extract_content_from_html(html_content)
#             document = {
#                 "text": text_content,
#                 "metadata": id
#             }
#             documents.append(document)
#     return documents

# def load_documents(cookie_val):
#     links = []
#     with open("links.txt", "r") as file:
#         for line in file:
#             link = line.strip()
#             if link.startswith("https://simpl.atlassian.net/wiki/spaces/TAC/pages/"):
#                 links.append(link)

#     doc_ids=extract_ids_from_links(links)
#     return fetch_documents_content(doc_ids,cookie_val)


def clear_embeddings(EMBEDDINGS_FOLDER):
    # Clear the embeddings folder
    if os.path.exists(EMBEDDINGS_FOLDER):
        shutil.rmtree(EMBEDDINGS_FOLDER)
    os.makedirs(EMBEDDINGS_FOLDER)

def check_embeddings_exist(EMBEDDINGS_FOLDER):
    # Check if the embeddings folder exists
    return os.path.exists(EMBEDDINGS_FOLDER)


def get_embeddings_timestamp(EMBEDDINGS_FOLDER):
    file_paths = glob.glob(os.path.join(EMBEDDINGS_FOLDER, "*"))
    if file_paths:
        latest_file = max(file_paths, key=os.path.getmtime)
        timestamp = os.path.getmtime(latest_file)
        return datetime.fromtimestamp(timestamp)
    else:
        return None


# def convert_text_to_page_content(array):
#     new_array = []
#     for item in array:
#         new_item = Document(
#             page_content=item["text"], metadata={"metadata": item["metadata"]}
#         )
#         new_array.append(new_item)
#     return new_array

load_dotenv()
URL = os.getenv("url")
USERNAME = os.getenv("username")
API_KEY = os.getenv("api_key")
SPACE_KEY = os.getenv("space_key")

def load_documents():
    loader = ConfluenceLoader(
    url="https://demoforsimp.atlassian.net/wiki", username="astay6318@gmail.com", api_key="ATATT3xFfGF0x_jtQEQg7v3DBEVB31ZSiSaC5Dsz51RW-7JEFvyChoauuYNqX6LZFylp8WWsrM3CfYqWc8nPbiQuHhXDUoShyY0S_hrZ7l7sMtKJ_lcsdP3kcGqcLuIJPgLibuIZ0aN-FvrBfA1pQtHUIsWLRjY14aYp8YBvUoXn7Cg_HQNiTKg=C84CD722")
    documents = loader.load(space_key="testing", include_attachments=True, limit=50)
    # loader = ConfluenceLoader(
    # url= URL, username= USERNAME, api_key= API_KEY)
    # documents = loader.load(space_key=SPACE_KEY, include_attachments=True, limit=50)
    return documents

def Document_Splitter(cookie_val):
    # documents_list = load_documents(cookie_val)
    documents= load_documents()
    # documents= convert_text_to_page_content(documents_list)  # to convert the documents into langchain.schema document
    chunk_size = 500
    chunk_overlap = 50
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap) 
    split_documents = text_splitter.split_documents(documents)    #to split documents
    return split_documents

def embed_documents_list(cookie_val):
    split_documents = Document_Splitter(cookie_val)
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    faissdb = FAISS.from_documents(split_documents, embeddings)
    return (embeddings,faissdb)

def store_embeddings(cookie_val):
    databases =  embed_documents_list(cookie_val)[1]
    # embeddings = embed_documents_list()[0]
    databases.save_local("faiss_index")
    # return loaded_database pkl
    
def return_embeddings(cookie_val):
    embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    store_embeddings(cookie_val)
    loaded_database = FAISS.load_local("faiss_index", embeddings)
    # use the database and fetch embeddings
    return loaded_database