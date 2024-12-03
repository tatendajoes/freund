#Secure API key
import os 
from dotenv import load_dotenv
from speech import Speech

#Getting conneted to gemini
import google.generativeai as genai

#Get API key
load_dotenv()
api_key= os.getenv('API_KEY')
#print(api_key)

#Configure
genai.configure(api_key=api_key)
model= genai.GenerativeModel(model_name='gemini-1.5-pro')


speech= Speech()
'''def conversation():
    chat=model.start_chat()
    while True:
        promt= input("")
        if promt=="STOP":
            break
        response= chat.send_message()
        print(response.text)
    '''
def conversation():
    chat=model.start_chat()
    while True:
        promt= input("")
        if promt=="STOP":
            break
        if speech.listen():
            print("processing")
            cond, text = speech.transcibe()
            if not cond==1:
                text = "Something went wrong"
        response= chat.send_message(text)
        speech.speak(response.text)

    
conversation()
    