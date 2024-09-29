#Secure API key
import os 
from dotenv import load_dotenv

#Getting conneted to gemini
import google.generativeai as genai

#Get API key
load_dotenv()
api_key= os.getenv('API_KEY')
#print(api_key)

#Configure
genai.configure(api_key=api_key)
model= genai.GenerativeModel(model_name='gemini-1.5-pro')



def conversation():
    chat=model.start_chat()
    while True:
        promt= input("")
        if promt=="STOP":
            break
        response= chat.send_message(promt)
        print(response.text)
    
    