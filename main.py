# import libraries for lemmatization and for read args
from time import time 
from typing import List
import pymorphy2
import sys
import re

# Init lemmetizator
morph = pymorphy2.MorphAnalyzer()

# all flags
all_flags: List[str] = ["-t", "-time", "-h", "--help"]

# word to normal state
def lemm_word(word: str) -> str:
  return morph.parse(word)[0].normal_form

def parse_args():
  return list(map(lambda x: x.lower(), re.sub(r'[^\w\s]', '', sys.argv[2]).split(" ")))

# words dictionary
map_words : dict = {}

# parsing text file
with open("./data/emoji_dict.txt") as data:
  """
  here we go through each line of the file 
  and split it into two values 
  using the split("-") function
  """
  for l in data.readlines():
    key, value = l.split("-")
    if len(key.split("/")) == 1:
      map_words[key] = value.replace("\n", "")
    else:
      key_words = key.split("/")
      for i in range(len(key_words)):
        map_words[key_words[i]] = f"{value}_{i}".replace("\n", "")



def translate(args: List[str]) -> str:
  ans = "" # answer variable and here we're return this

  for arg in args:
    for key in map_words.keys():
      if lemm_word(arg) in key.split("/"):
        # if word for 1per or 2per we're adding spec. emoji
        if "1per" in morph.parse(arg)[0].tag and "я" not in args: ans += "👆🏼"
        elif "2per" in morph.parse(arg)[0].tag and "ты" not in args: ans += "👇🏻"
        
        if "_" in map_words[key]:
          ans += map_words[key][:-2] + " "
        else:
          ans += map_words[key] + " "

  # if the sentence is interrogative then add a question mark
  if sys.argv[2][-1] == "?" : ans += "❓"

  return ans

def optimize_translate(args: List[str]) -> str:
  ans = ""
  for arg in args:
    lemm_arg = lemm_word(arg)
    try:
      if "_" in map_words[lemm_arg]:
        ans += map_words[lemm_arg][:-2] + " "
      else:
        ans += map_words[lemm_arg] + " "
    
      if "1per" in morph.parse(arg)[0].tag and "я" not in args: ans += "👆🏼"
      elif "2per" in morph.parse(arg)[0].tag and "ты" not in args: ans += "👇🏻"

    except KeyError:
      pass
  
  if sys.argv[2][-1] == "?" : ans += "❓"

  return ans

# you can translate only if flat -t
if sys.argv[1] not in all_flags:
  print(f"Unexpected flag '{sys.argv[1]}'")

elif sys.argv[1] == "-t":
  print(optimize_translate(parse_args()))
  
elif sys.argv[1] == "-time":
  t1 = time()
  print(optimize_translate(parse_args()))
  print(f"(new algoritmh)\n{time() - t1}s")

  print("\n")

  t2 = time()
  print(translate(parse_args()))
  print(f"(old algoritmh)\n{time() - t2}s")

elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
  print("""
    help: '-h' or '--help'
    translate text to emoji: '-t'
    time test: '-time'
  """)
