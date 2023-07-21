LLM Based Search API is a Flask app that allows users to ask questions specific to their documents in a completely private environment with no data leakage. It is powered by Langchain, HuggingFace, Faiss, Dolly, and Flask.

## Environment Setup
Before you can run the LLM Based Search API, ensure you have the following prerequisites installed:
Python, Virtual environment and ThunderClient/Postman
### Installing Python, Virtual environment and ThunderClient/Postman
1. Python:Visit the official Python website: [python.org](https://www.python.org)   
2. Virtual Environment: Install virtual environment using the following command:  
``` 
pip install virtualenv
```      
3. Postman/ThunderClient: Install Postman from the official site of Postman: [Postman](https://www.postman.com/downloads/) or search for Thunder Client in the `VS Code` extensions and install it.

### Configuring the Environment
Follow these steps to configure your environment and run the LLM Based Search API:  

Create your virtual environment using the following command:  
```
python3 -m venv myenv
```

Start your virtual environment:  
For windows:  
```
myenv\Scripts\activate
```   

For Mac:  
```
source myenv/bin/activate
```  

Now to run the code you first need to install all the requirements:  
```
pip install -r requirements.txt
```    

**Note:**  The first you run the model you will need internet connection to load the required models to run the application.

## Ask questions on your documents, locally
To start using the LLM Based Search API, follow these steps:  

1. Run the server using the command:
```
python src/main.py 
```  

After running this command you will be given an output that the server has started running at ```
http://127.0.0.1:5000
```.     
**Note:** The first time you run the app, it may take some time to create the embeddings, which will be done once and updated after 7 days of the most recently modified file. Once the embeddings are created, you can proceed with the next step.
2. Perform a GET request on Thunder Client or Postman to ensure the server is ready for queries. The expected output should be: **Good to Go! Start searching!**  

### Making Queries
To ask questions specific to your documents, make a GET request to the following URL:  
```
http://127.0.0.1:5000\api\search
```.   

Feel free to explore and integrate this API into your projects. If you encounter any issues or have suggestions for improvements, please open an issue or contribute to the project.

Thank you for using LLM Based Search API! If you have any questions or need further assistance, don't hesitate to reach out to me.





