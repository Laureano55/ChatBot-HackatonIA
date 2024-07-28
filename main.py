import google.generativeai as genai
import os

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.0-pro-latest')
while True:
    text = input("Enter a prompt: ")
    response = model.generate_content(text)
    print(response.text)


print(response.text)