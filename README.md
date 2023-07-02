This is a Flask app where users can ask questions related to their documents rather than getting the answers depending on the whole app. 100% private and no data leakage.

Built with LangChain, HuggingFace Embeddings, Faiss, Dolly and Flask.

## Environment Setup
First you need to have python installed and virtualenv installed.

### Installing Python, Virtual environment and ThunderClient/Postman
To install python visit the official site of python: [python.org](https://www.python.org) 

To install virtual environment run the following command:  
`pip install virtualenv`

To install Postman visit the official site of Postman: [Postman](https://www.postman.com/downloads/)

Thunder Client:  In the extensions of `VS Code` look for Thunder Client and install it.

### Configuring the Environment
Create your virtual environment using the following command:  
`python3 -m venv myenv `

Start your virtual environment:  
For windows:  
`myenv\Scripts\activate` 

For Mac:  
`source myenv/bin/activate`

Now to run the code you first need to install all the requirements:  
`pip install -r requirements.txt `

**Note:**  The first you run the model you will need internet connection to load the required models to run the application.

## Ask questions on your documents, locally

First run the command:  
`python src/main.py`

After running this command you will be given an output that the server has started running on `http://127.0.0.1:5000`.   
**Note:** When running the app for the first time it will take some time to create the embeddings (will take time to create embeddings after 7 days of the most recent modified file).
Once the embeddings are done, you can do a `GET` request on ThunderClient or Postman and should recieve an output as:  **Good to Go! Start searching!**

### Putting a Query
To start searching you should add `/api/search` at the end of the link:`http://127.0.0.1:5000` .  
Which should be like this:  
`http://127.0.0.1:5000/api/search`




