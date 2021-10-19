# import libraries for lemmatization and for read args
from typing import List
import pymorphy2
import sys
import re

# Init lemmetizator
morph = pymorphy2.MorphAnalyzer()

# word to normal state
def lemm_word(word: str) -> str:
  return morph.parse(word)[0].normal_form

def parse_args():
  return re.sub(r'[^\w\s]', '', sys.argv[2]).split(" ")

# words dictionary
map_words : dict = {}

with open("./data/emoji_dict.txt") as data:
  for l in data.readlines():
    key, value = l.split("-")
    map_words[key] = value.replace("\n", "")


def translate(args):
  ans = ""
  for arg in args:
    for key in map_words.keys():
      if lemm_word(arg) in key.split("/"):
        if "1per" in morph.parse(arg)[0].tag and arg != "я": ans += "👆🏼"
        elif "2per" in morph.parse(arg)[0].tag and arg != "ты": ans += "👇🏻"
        
        ans += map_words[key] + " "

        if sys.argv[2][-1] == "?" : ans += "❓"
  return ans



if sys.argv[1] == "-t":
  print(translate(parse_args()))
