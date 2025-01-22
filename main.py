# pip install pyTelegramBotAPI
# pip install python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_KEY = os.getenv("TELEGRAM_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")




"""
Install an additional SDK for JSON schema support Google AI Python SDK

$ pip install google.ai.generativelanguage
"""

import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

genai.configure(api_key=GEMINI_API_KEY)


# Create the model
generation_config = {
  "temperature": 0.2,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_schema": content.Schema(
    type = content.Type.OBJECT,
    enum = [],
    required = ["Hospital Name", "Address", "Phone Number"],
    properties = {
      "Hospital Name": content.Schema(
        type = content.Type.STRING,
      ),
      "Address": content.Schema(
        type = content.Type.STRING,
        # items = content.Schema(
        #   type = content.Type.STRING,
        # ),
      ),
      "Phone Number": content.Schema(
        type = content.Type.STRING,
      ),
      "Amenities": content.Schema(
        type = content.Type.STRING,
      ),
      "Timings": content.Schema(
        type = content.Type.STRING,
      ),
      "Maps link": content.Schema(
        type = content.Type.STRING,
      ),
      "Extra note": content.Schema(
        type = content.Type.STRING,
      ),
    },
  ),
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction="You're a professional healthcare assistant with access to google maps and search. When user gives a city name you have to output details of any one good hospital in that region in a structure output mentioned, only one. Other irrelavant questions from user should be politely unanswered",
)

chat_session = model.start_chat(
  history=[
  ]
)

import telebot

bot = telebot.TeleBot("TELEGRAM_KEY")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	response = chat_session.send_message(message.text)
	print(response.text)
	bot.send_message(message.chat.id, response.text)



bot.infinity_polling()