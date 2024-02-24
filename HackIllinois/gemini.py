
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

genai.configure(api_key = "AIzaSyB7AZkwAHmzWcs_2yiU4TbyUbb8GIQNB68")


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def error_lookup(prompt) :
  model = genai.GenerativeModel('gemini-pro')
  str = "I'm encountering this error in my code: "
  str += prompt
  response = model.generate_content(str)
  print("\n",response.text)


    

