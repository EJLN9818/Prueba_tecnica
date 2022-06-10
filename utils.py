import pandas as pd
import time
import hashlib
import json
import sqlite3

def process_data(countries):
    data = {
        'Region': [],
        'City Name': [],
        'Language': [],
        'Time': [],
    }

    data_time_execution = {
        'times': [],
        'total_time': 0,
        'average_time': 0,
        'min_time':0,
        'max_time':0
    }

    for country in countries:
        start = time.time()
        data['Region'].append(country['region'])
        data['City Name'].append(country['name']['common'])
        
        lenguages =  ', '.join(list(country.get('languages', {'None': 'No lenguages'}).values()))
        data['Language'].append(generate_hash(lenguages))
        time_finish = f'{time.time() - start:.10f}'
        data_time_execution['times'].append(float(time_finish))
        data['Time'].append(time_finish + ' ms')

    df = pd.DataFrame(data, index=['' for x in range(0,len(data['Region']))])

    df_time_execution = pd.DataFrame(data_time_execution)
    df_time_execution['total_time'] = df_time_execution['times'].sum()
    df_time_execution['average_time'] = df_time_execution['total_time'].mean()
    df_time_execution['min_time'] = df_time_execution['times'].min()
    df_time_execution['max_time'] = df_time_execution['times'].max()
    del df_time_execution['times']
    df_time_execution.drop(range(1,len(df_time_execution)), inplace=True)
    return df.sort_values(by=['Region', 'City Name']), df_time_execution

def generate_hash(lenguages):
    hash_object = hashlib.sha1(bytes(lenguages, 'utf-8'))
    return hash_object.hexdigest()

def generate_json(df):
    result = df.to_json(orient="split")
    parsed = json.loads(result)
    return json.dumps(parsed, indent=4)  

def generate_sqlite(df):
    conn = sqlite3.connect('test_db.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS countries (region text, city_name text, lenguages text, time text)')
    conn.commit()
    df.to_sql('countries', conn, if_exists='replace', index = False)
    c.execute('SELECT * FROM countries')

    for row in c.fetchall():
        print (row)