import google.generativeai as genai
import os
import markdown


genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.0-pro-latest')



def read_markdown_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    markdown_data = file.read()
  return markdown_data



# Example usage
file_path = "MatriculaUN_data.md"
markdown_content = read_markdown_file(file_path)





while True:
    text = input("Enter a prompt: ")
    prompt = f"""Tu nombre es Sofía, la asistente de IA de la Universidad del Norte, 
    y tu trabajo es responder preguntas relacionadas a la universidad basado en el siguiente contenido.
    Sé amable con el usuario e interpreta las preguntas bien. Puedes hablar con el usuario naturalmente,
    pero si hace una pregunta no está relacionada con el contenido, responde que no puedes responderlas. 
    No menciones NUNCA que sacas esta información de un contenido proporcionado. En caso de que la pregunta 
    no tenga relación, solo di eso, o si la pregunta tiene que ver pero no conoces la respuesta,
    di que no tienes esa información.\n{markdown_content}\n{text}"""
    response = model.generate_content(prompt)
    print(response.text)