with open("./data/emoji_dict.txt") as data:
  for l in data.readlines():
    key, value = l.split("-")
    print(key, value)