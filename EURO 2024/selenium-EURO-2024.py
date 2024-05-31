from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_matches_1959():
    print('\nGetting the Matches of Copa America 1959')
    
    web1 = 'https://es.wikipedia.org/wiki/Campeonato_Sudamericano_1959_(Argentina)'
    web2 = 'https://es.wikipedia.org/wiki/Campeonato_Sudamericano_1959_(Ecuador)'

    # Extract data from Argentina page
    driver.get(web1)
    matches_argentina = driver.find_elements(by='xpath', value='//td[@align="right"]/..| //td[@style="text-align:right;"]/..')

    home_argentina = []
    score_argentina = []
    away_argentina = []

    for game in matches_argentina:
        cells = game.find_elements(by='xpath', value='./td')
        if len(cells) >= 4:
            home_argentina.append(cells[1].text.strip())
            score_argentina.append(cells[2].text.strip())
            away_argentina.append(cells[3].text.strip())

    dict_football_argentina = {'home': home_argentina, 'score': score_argentina, 'away': away_argentina}
    df_football_argentina = pd.DataFrame(dict_football_argentina)
    df_football_argentina['year'] = 1959

    # Extract data from Ecuador page
    driver.get(web2)
    matches_ecuador = driver.find_elements(by='xpath', value='//td[@align="right"]/..| //td[@style="text-align:right;"]/..')

    home_ecuador = []
    score_ecuador = []
    away_ecuador = []

    for game in matches_ecuador:
        cells = game.find_elements(by='xpath', value='./td')
        if len(cells) >= 4:
            home_ecuador.append(cells[1].text.strip())
            score_ecuador.append(cells[2].text.strip())
            away_ecuador.append(cells[3].text.strip())

    dict_football_ecuador = {'home': home_ecuador, 'score': score_ecuador, 'away': away_ecuador}
    df_football_ecuador = pd.DataFrame(dict_football_ecuador)
    df_football_ecuador['year'] = 1959

    # Combine data from Argentina and Ecuador
    df_1959 = pd.concat([df_football_argentina, df_football_ecuador], ignore_index=True)
    return df_1959

def get_matches(year):
    print(f'\nGetting the Matches of EURO {year}')
    
    #https://en.wikipedia.org/wiki/1964_European_Nations%27_Cup

    #https://en.wikipedia.org/wiki/UEFA_Euro_1968
    #https://en.wikipedia.org/wiki/UEFA_Euro_1972
    #https://en.wikipedia.org/wiki/UEFA_Euro_2024

    if year <= 1964:
        web = f'https://en.wikipedia.org/wiki/{year}_European_Nations%27_Cup'
    else:
        web = f'https://en.wikipedia.org/wiki/UEFA_Euro_{year}'

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

# Extract data for all Copa America years
years = [1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 
         1996, 2000, 2004, 2008, 2012, 2016, 2020]

Euro = [get_matches(year) for year in years]


# Concatenate all DataFrames into one final DataFrame
df_Euro = pd.concat(Euro, ignore_index=True)
print(df_Euro[df_Euro['year'] == 2012])  # Debugging: print the rows for the year 1959
df_Euro.to_csv('EURO_Historical_Data.csv', index=False)