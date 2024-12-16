import os
import google.generativeai as genai
from config import apikey
import webbrowser

genai.configure(api_key=apikey)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config = generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

def search_api(query):
  response = chat_session.send_message(query)
  # print(f"API Response: {response.text}")
  return response.text