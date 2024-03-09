import re
import requests

website = 'https://quotes.toscrape.com/'
result = requests.get(website)
content = result.text

print(content)