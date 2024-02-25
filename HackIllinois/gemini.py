
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

genai.configure(api_key = "AIzaSyB7AZkwAHmzWcs_2yiU4TbyUbb8GIQNB68")


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def error_lookup(prompt) :
  model = genai.GenerativeModel('gemini-pro')
  str = "I'm encountering this error in my code: "
  str += prompt
  response = model.generate_content(str)
  print(bcolors.OKBLUE + "\n",response.text,"\n" + bcolors.ENDC)
  return response.text

def tips(error, code) :
  model = genai.GenerativeModel('gemini-pro')
  str = "I'm encountering this error in my code: "
  str += error
  str += ". Give me some tips and potential code fixes based on my error and the following code: "
  for i in code:
    str += i
    str += "\n"
  response = model.generate_content(str)
  print(bcolors.OKCYAN + "\n",response.text,"\n" + bcolors.ENDC)
  return response.text

def links(error, code) :
  model = genai.GenerativeModel('gemini-pro')
  str = "I'm encountering this error in my code: "
  str += error
  str += ". Give me some links and resources I can learn from based on my error and the following code: "
  for i in code:
    str += i
    str += "\n"
  response = model.generate_content(str)
  print(bcolors.OKGREEN + "\n",response.text,"\n" + bcolors.ENDC)
  return response.text
