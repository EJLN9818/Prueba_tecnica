print('Welcome to ')
print('Loading...')

from install_packages import install_packages
install_packages(['requests', 'pandas'])

from utils import process_data, generate_json, generate_sqlite
from apis import get_countries, get_country_for_name, get_countries_for_region

def first_options():
    print('''
    What do you want?
    (1) search one country by name
    (2) search for all countries by region
    (3) search all countries
    ''')
    choice =  input('Choice: ')
    countries = None

    if choice == '1':
        name = input('Name: ')
        countries = get_country_for_name(name)
        if not countries:
            print('Country not found')
    elif choice == '2':
        region = input('Region: ')
        countries = get_countries_for_region(region)
        if not countries:
            print('Countries not found')
    elif choice == '3':
        countries = get_countries()
        if not countries:
            print('No countries found')
    

    if countries:
        df, df_time_execution = process_data(countries)
        print(df)
        print('\n****************************************************\n')
        print(df_time_execution)
        print('\n****************************************************\n')
        
        second_options(df)

def second_options(df):
    print('''
    What do you want?
    (1) return firsts options
    (2) generate JSON
    (3) generate SQLite
    ''')
    choice = input('Choice: ')
    if choice == '1':
        first_options()
    elif choice == '2':
        print('Generating JSON...')
        print(generate_json(df))
    elif choice == '3':
        print('Generating SQLite...')
        print(generate_sqlite(df))
    else:
        goodbye()

def goodbye():
    print('Goodbye!')

first_options()