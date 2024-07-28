import google.generativeai as genai
import os


genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.0-pro-latest')



def read_markdown_file(file_path):
  with open(file_path, 'r', encoding='utf-8') as file:
    markdown_data = file.read()
  return markdown_data



# Example usage
file_path = "MatriculaUN_data.md"
markdown_content = read_markdown_file(file_path)

history = ""
i = 1


while True:
    text = input("Enter a prompt: ")
    


    prompt = f"""Tu nombre es Sofía, la asistente de IA de la Universidad del Norte, 
    y tu trabajo es responder preguntas relacionadas a la universidad basado en el siguiente contenido.
    Sé amable con el usuario e interpreta las preguntas bien. Puedes hablar con el usuario naturalmente,
    pero si hace una pregunta no está relacionada con el contenido, responde que no puedes responderlas.
    Puedes hablarles de cosas que estén en el historial.
    No menciones NUNCA que sacas esta información de un contenido proporcionado. \n Información:\n {markdown_content} \n Historial de la conversación: \n {history}
    \n Pregunta del usuario:\n{text}"""

    response = model.generate_content(prompt)

    history = history + f"Pregunta {i}: \n{text} \n Respuesta {i}:\n{response.text}"

    print(response.text)
    i += 1