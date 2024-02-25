
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

def tips(error, code) :
  model = genai.GenerativeModel('gemini-pro')
  str = "I'm encountering this error in my code: "
  str += error
  str += ". Give me some tips and potential code fixes based on my error and the following code: "
  for i in code:
    str += i
    str += "\n"
  response = model.generate_content(str)
  print("\n",response.text)

def links(error, code) :
  model = genai.GenerativeModel('gemini-pro')
  str = "I'm encountering this error in my code: "
  str += error
  str += ". Give me some links and resources I can learn from based on my error and the following code: "
  for i in code:
    str += i
    str += "\n"
  response = model.generate_content(str)
  print("\n",response.text)
