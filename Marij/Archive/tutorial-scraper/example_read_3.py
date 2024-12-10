import json

# Open the file with UTF-8 encoding
with open('quotes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Access data
for item in data:
    print(item['text'])  # Prints every quote
    print(item['author'])  # Prints the author's name
