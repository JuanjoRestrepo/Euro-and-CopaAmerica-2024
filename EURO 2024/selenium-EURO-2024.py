import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

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

    driver.get(web)
    matches = driver.find_elements(by='xpath', value='//td[@align="right"]/.. | //td[@style="text-align:right;"]/..')

    home = []
    score = []
    away = []

    for game in matches:
        home.append(game.find_element(by='xpath', value='./td[2]').text)
        score.append(game.find_element(by='xpath', value='./td[3]').text)
        away.append(game.find_element(by='xpath', value='./td[4]').text)

    dict_football = {'home': home, 'score': score, 'away': away}
    df_football = pd.DataFrame(dict_football)
    df_football['year'] = year

    return df_football

# Extract data for all Copa America years
years = [1960, 1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 
         1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024]

CopaAmerica = []

# Iterate through the years and call the appropriate function
for year in years:
    if year == 1959:
        df_1959 = get_matches_1959()
        print(df_1959.head())  # Debugging: print the first few rows of the 1959 dataframe
        CopaAmerica.append(df_1959)
    else:
        df_year = get_matches(year)
        CopaAmerica.append(df_year)

driver.quit()

# Concatenate all DataFrames into one final DataFrame
df_CopaAmerica = pd.concat(CopaAmerica, ignore_index=True)
print(df_CopaAmerica[df_CopaAmerica['year'] == 1959])  # Debugging: print the rows for the year 1959
df_CopaAmerica.to_csv('EURO_Historical_Data.csv', index=False)