import re

SHOES = re.compile(r'[s|S]{1}["hoe"]{1}[s]*|[w|W]{1}["edge"]{1}[s]*|[b|B]{1}["oot"]{1}["ie"]?[s]*|[p|P]{1}["ump"]{1}[s]*|[h|H]{1}["eel"]{1}[s]*|[s|S]{1}["neaker"]{1}[s]*')

JEWELRY = re.compile(r'[b|B]{1}["racelet"]{1}[s]*|[n|N]{1}["ecklace"]{1}[s]*|[r|R]{1}["ing"]{1}[s]*|[e|E]{1}["arring"]{1}[s]*')

BAGS = re.compile(r'[b|B]{1}["ag"]{1}[s]*')

ACCESSORIES = re.compile(r'[s|S]{1}["unglasses"]{1}|[h|H]{1}["at"]{1}[s]*')
