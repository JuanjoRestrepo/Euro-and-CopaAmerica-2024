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
    print(f'\nGetting the Matches of Copa America {year}')

    if year >= 1975:
        web = f'https://es.wikipedia.org/wiki/Copa_Am%C3%A9rica_{year}'
    elif year <= 1967:
        web = f'https://es.wikipedia.org/wiki/Campeonato_Sudamericano_{year}'
    else:
        return pd.DataFrame()  # Return an empty DataFrame if the year is not valid

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
years = [1916, 1917, 1919, 1920, 1921, 1922, 1923, 1924, 1925, 1926,
         1927, 1929, 1935, 1937, 1939, 1941, 1942, 1945, 1946, 1947,
         1949, 1953, 1955, 1956, 1957, 1959, 1963, 1967, 1975, 1979,
         1983, 1983, 1987, 1989, 1991, 1993, 1995, 1997, 1999, 2001,
         2004, 2007, 2011, 2015, 2016, 2019, 2021]

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
df_CopaAmerica.to_csv('Copa_America_Historical_Data.csv', index=False)