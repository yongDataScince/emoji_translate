# import libraries for lemmatization and for read args
from typing import List
import pymorphy2
import sys
import re

# Init lemmetizator
morph = pymorphy2.MorphAnalyzer()

# all flags
all_flags: List[str] = ["-t", "-h", "--help"]

# word to normal state
def lemm_word(word: str) -> str:
  return morph.parse(word)[0].normal_form

def parse_args() -> str:
  return re.sub(r'[^\w\s]', '', sys.argv[2]).split(" ")

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
    map_words[key] = value.replace("\n", "")


def translate(args) -> str:
  ans = ""
  for arg in args:
    for key in map_words.keys():
      if lemm_word(arg) in key.split("/"):
        # if word for 1per or 2per we're adding spec. emoji
        if "1per" in morph.parse(arg)[0].tag and "я" not in args: ans += "👆🏼"
        elif "2per" in morph.parse(arg)[0].tag and "ты" not in args: ans += "👇🏻"
        
        ans += map_words[key] + " "

  # if the sentence is interrogative then add a question mark
  if sys.argv[2][-1] == "?" : ans += "❓"

  return ans


# you can translate only if flat -t
if sys.argv[1] not in all_flags:
  print(f"Unexpected flag '{sys.argv[1]}'")

elif sys.argv[1] == "-t":
  print(translate(parse_args()))

elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
  print("""
    help: '-h' or '--help'
    translate text to emoji: '-t'
  """)