
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

genai.configure(api_key = "AIzaSyB7AZkwAHmzWcs_2yiU4TbyUbb8GIQNB68")

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("How do you win a Hackathon?")
print(response.text)


    

