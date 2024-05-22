from bs4 import BeautifulSoup
import requests
import pandas as pd

# Extraemos la data de todos los mundiales desde 1930 hasta 2018
# Haremos el Webscrapping para obtener estos datos con 'requests' y bs4
years = [2024]

def get_matches(year):
  if year == '2024':
    web =  f'https://en.wikipedia.org/wiki/{year}_Copa_Am%C3%A9rica'

  response = requests.get(web)
  content = response.text #contenido html de la pagina
  soup = BeautifulSoup(content, 'lxml')

  matches = soup.find_all('div', class_='footballbox')

  home = []
  score = []
  away = []

  for game in matches:
      home.append(game.find('th', class_='fhome').get_text())
      score.append(game.find('th', class_='fscore').get_text())
      away.append(game.find('th', class_='faway').get_text())

  dict_football = {'home': home,
                  'score': score,
                  'away': away}

  df_football = pd.DataFrame(dict_football)
  df_football['year'] = year
  return df_football


# Data del mundial Qatar 2022
df_fixture = get_matches('2024')
df_fixture = df_fixture
df_fixture.to_csv('Copa_America_Fixture.csv', index=False)