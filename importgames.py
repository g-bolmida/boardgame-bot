import db
import csv

def add_games_db(user: str, filename: str):
    print(f"Adding games from {user} to the database")
    with open(filename, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            # Access and print the values for 'objectname', 'minplayers', and 'maxplayers'
            objectname = row['objectname']
            objectid = row['objectid']
            minplayers = row['minplayers']
            maxplayers = row['maxplayers']
            minplaytime = row['minplaytime']
            maxplaytime = row['maxplaytime']

            print(f"Object Name: {objectname}, ID: {objectid}, Min Players: {minplayers}, Max Players: {maxplayers}, Min Playtime: {minplaytime}, Max Playtime: {maxplaytime}")
