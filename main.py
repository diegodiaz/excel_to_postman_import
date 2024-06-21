import pandas as pd
import json

def parse_endpoint(row):
    host = "{{host}}"
    
    return {
        "name": row['name'] if row['name'] is not None else f"{row['Controller']} {row['path']}",
        "request": {
            "method": row['method'],
            "header": [],
            "url": {
                "raw": f"{host}{row['path'] if row['path'] is not None else ''}",
                "host": [host],
                "path": [row['path'] if row['path'] is not None else '']
            },
            "description": row.get('description', '')
        },
        "response": []
    }


def run():
    # read excel and transform in a dataframe
    df = pd.read_excel('./data/Endpoints.xlsx')

    # print the dataframe
    print(df)

    # create a list to store all json objects
    json_list = []
    host = "{{host}}"

    # replace empty values with None
    df = df.replace(r'^\s*$', None, regex=True)

    # replace NaN values with None
    df = df.where(pd.notnull(df), None)

    collections = {}

    collections = {}

    for _, row in df.iterrows():
        collection_name = row['Controller']
        if collection_name not in collections:
            collections[collection_name] = {
                "name": collection_name,
                "item": []
            }
        
        collections[collection_name]["item"].append(parse_endpoint(row))

    # Convertir a una lista de colecciones
    postman_collections = {
        "info": {
            "name": "API Documentation",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": list(collections.values())
    }

    # Guardar las colecciones como un archivo JSON
    with open('./data/postman_collections.json', 'w') as f:
        json.dump(postman_collections, f, indent=4)

    
    print('File created successfully')

if __name__ == '__main__':
    run()