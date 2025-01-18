from flask import Flask, render_template
from data import schedule, scores, points_table, mvp_table, Home1, rules, teams, schedule, gallery, sponsor, mvp
import csv
import io
from google.cloud import storage

app = Flask(__name__)

BUCKET_NAME = "pblbucket"
SCORES_FILE ="Scores.csv"
MVP_FILE = "Playerstat.csv"
is_Cloud = True


# @app.route("/")
#def index():
#   return render_template("index.html", schedule=schedule)

@app.route("/")
def home1_page():
    return render_template("Home1.html", Home1=Home1)

@app.route("/scores")
def scores_page():
    return render_template("score.html", matches=GetScores())

@app.route("/points_table")
def points():
    # Path to the CSV file
    csv_file_path = "Pointtable.csv"
    
    # Read the CSV data
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    # Extract headers and rows
    headers = data[0]
    rows = data[1:]
    return render_template("point_table.html", headers=headers, rows=rows)


@app.route("/rules")
def rules_page():
    return render_template("rules.html", rules=rules)

@app.route("/teams")
def teams_page():
    return render_template("teams.html", teams=teams)

@app.route("/schedule")
def schedule_page():
    return render_template("schedule.html", schedule=schedule)

@app.route("/gallery")
def gallery_page():
    return render_template("gallery.html", gallery=gallery)

@app.route("/sponsor")
def sponsor_page():
    return render_template("sponsor.html", sponsor=sponsor)

@app.route("/mvp")
def test():

    if is_Cloud :
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(MVP_FILE)
            # Download the CSV data as a string
        csv_data = blob.download_as_text()
                # Parse the CSV data
        csv_reader = csv.DictReader(io.StringIO(csv_data))
        csv_reader.fieldnames = [header.strip().lower() for header in csv_reader.fieldnames]

        data = list(csv_reader)
    
        # Extract headers and rows
        headers = csv_reader.fieldnames
        rows = data

        return render_template("mvp.html", headers=headers, rows=rows)

    else: 
        # Path to the CSV file
        csv_file_path = "Playerstat.csv"
        # Read the CSV data
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        # Extract headers and rows
        headers = data[0]
        rows = data[1:]

        return render_template("mvp.html", headers=headers, rows=rows)



def GetScores():
# Open the CSV file and read its contents
    matches = []
    
    if is_Cloud :
       storage_client = storage.Client()
       bucket = storage_client.bucket(BUCKET_NAME)
       blob = bucket.blob(SCORES_FILE)
        # Download the CSV data as a string
       csv_data = blob.download_as_text()
            # Parse the CSV data
       csv_reader = csv.DictReader(io.StringIO(csv_data))
       csv_reader.fieldnames = [header.strip().lower() for header in csv_reader.fieldnames]
       matches = []
       for row in csv_reader:
                # Create a match dictionary to store match details
            match = {
                    "team_1": row['team_1'],
                    "team_2": row['team_2'],
                    "games": [],
                    "match_type":row['match_type']
                }
                
                # Dynamically add all scores (both singles and doubles) to the 'games' list
            for i in range(1, 5):  # Up to 3 matches (singles and doubles)
                singlesKids_key = f'singlesKids_{i}_score'
                doublesKids_key = f'doubleKids_{i}_score'
                doubleKidsAdults_Key =  f'doubleKidsAdults_{i}_score'
                singlesmens_key = f'singlesmens_{i}_score'
                doublesmens_key = f'doublesmens_{i}_score'
                doubleswomens_key = f'doubleswomens_{i}_score'
                doublesmixed_key = f'doublesmixed_{i}_score'

                if singlesKids_key in row and row[singlesKids_key]:
                    match["games"].append({"type": f"Kids Singles {i}", "score": row[singlesKids_key]})

                if doublesKids_key in row and row[doublesKids_key]:
                   match["games"].append({"type": f"Kids Doubles {i}", "score": row[doublesKids_key]})

                if doubleKidsAdults_Key in row and row[doubleKidsAdults_Key]:
                    match["games"].append({"type": f"Adult/Kids Doubles {i}", "score": row[doubleKidsAdults_Key]})

                if singlesmens_key in row and row[singlesmens_key]:
                    match["games"].append({"type": f"Mens Singles {i}", "score": row[singlesmens_key]})

                if doublesmens_key in row and row[doublesmens_key]:
                    match["games"].append({"type": f"Mens Doubles {i}", "score": row[doublesmens_key]})

                if doubleswomens_key in row and row[doubleswomens_key]:
                    match["games"].append({"type": f"Womens Doubles {i}", "score": row[doubleswomens_key]})
                            
                if doublesmixed_key in row and row[doublesmixed_key]:
                    match["games"].append({"type": f"Mixed Doubles {i}", "score": row[doublesmixed_key]})
                        # Add match data to the matches list
            matches.append(match)

    else:
# Open the CSV file and read the contents
        with open('scores.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            matches = []
            for row in csv_reader:
                # Create a match dictionary to store match details
                print (row)
                match = {
                    "team_1": row['team_1'],
                    "team_2": row['team_2'],
                    "games": [],
                    "match_type":row['match_type']
                }
                
                # Dynamically add all scores (both singles and doubles) to the 'games' list
                for i in range(1, 5):  # Up to 3 matches (singles and doubles)
                    singlesKids_key = f'singlesKids_{i}_score'
                    doublesKids_key = f'doubleKids_{i}_score'
                    doubleswomens_key = f'doubleswomens_{i}_score'
                    doubleKidsAdults_Key =  f'doubleKidsAdults_{i}_score'
                    doublesmixed_key = f'doublesmixed_{i}_score'
                    singlesmens_key = f'singlesmens_{i}_score'
                    doublesmens_key = f'doublesmens_{i}_score'
                    

                    if singlesKids_key in row and row[singlesKids_key]:
                        match["games"].append({"type": f"Kids Singles {i}", "score": row[singlesKids_key]})

                    if doublesKids_key in row and row[doublesKids_key]:
                        match["games"].append({"type": f"Kids Doubles {i}", "score": row[doublesKids_key]})

                    if doubleswomens_key in row and row[doubleswomens_key]:
                        match["games"].append({"type": f"Womens Doubles {i}", "score": row[doubleswomens_key]})

                    if doubleKidsAdults_Key in row and row[doubleKidsAdults_Key]:
                        match["games"].append({"type": f"Adult/Kids Doubles {i}", "score": row[doubleKidsAdults_Key]})

                    if doublesmixed_key in row and row[doublesmixed_key]:
                        match["games"].append({"type": f"Mixed Doubles {i}", "score": row[doublesmixed_key]})

                    if singlesmens_key in row and row[singlesmens_key]:
                        match["games"].append({"type": f"Mens Singles {i}", "score": row[singlesmens_key]})

                    if doublesmens_key in row and row[doublesmens_key]:
                        match["games"].append({"type": f"Mens Doubles {i}", "score": row[doublesmens_key]})
                   
                        # Add match data to the matches list
                matches.append(match)
    print("123")
    for match in matches:
        match["games"] = sort_games(match["games"])
        print(match)
    return matches

def sort_games(games):
    # Define the order of game types
    order = ["Kids Singles 1", "Kids Doubles 1","Kids Doubles 2" ,"Womens Doubles 1","Adult/Kids Doubles 1","Mixed Doubles 1","Adult/Kids Doubles 2",
             "Mens Singles 1", "Mens Doubles 1","Mens Doubles 2" ,"Mens Doubles 3","Mens Doubles 4" ]
    return sorted(games, key=lambda x: (next((i for i, item in enumerate(order) if x["type"].startswith(item)), len(order)), x["type"]))

if __name__ == "__main__":
    app.run(debug=True)




