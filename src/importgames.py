import db
import csv

def add_games_db(user: str, filename: str):
    # create db session
    Session = db.sessionmaker(bind=db.engine)
    session = Session()
    
    username = session.query(db.User).filter(db.User.name == user).first()
    if username is None:
        username = db.User(name=user)
        session.add(username)
        session.commit()
        print("Added user: "+user)
    else:
        print("User already exists: "+user)

    with open(filename, mode='r', newline='') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            objectname = row['objectname']
            objectid = row['objectid']
            minplayers = row['minplayers']
            maxplayers = row['maxplayers']
            minplaytime = row['minplaytime']
            maxplaytime = row['maxplaytime']

            if session.query(db.Games).filter(db.Games.name == objectname).first() is None:
                newgame = db.Games(name=objectname, bgg_url="https://boardgamegeek.com/boardgame/"+objectid, min_players=minplayers, max_players=maxplayers, min_playtime=minplaytime, max_playtime=maxplaytime)
                session.add(newgame)
                session.commit()
                print("Added game: "+objectname)
            else:
                print("Game already exists: "+objectname)

            game = session.query(db.Games).filter(db.Games.name == objectname).first()
            if game:
                if game not in username.games:
                    username.games.append(game)
                    session.commit()
                    print("Added game to " + user + ": "+objectname)
                else:
                    print("User already owns this game.")

    session.close()
