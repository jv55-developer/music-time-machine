import requests
from bs4 import BeautifulSoup

song_time = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{song_time}/")
webpage = response.text
soup = BeautifulSoup(webpage, 'html.parser')

print(soup.prettify())
