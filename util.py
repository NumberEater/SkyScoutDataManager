import sqlite3
import os
import os.path

def convertDataAfterMatch(match: int):
    conn = sqlite3.connect("match_data.db")
    query = f"SELECT * FROM MatchData WHERE MatchNumber > {match}"
    convertSQLToCSVFile(conn, query, f"match_data_after_{match}.csv")
    conn.close()

def convertAllMatchData():
    conn = sqlite3.connect("match_data.db")
    query = "SELECT * FROM MatchData"
    convertSQLToCSVFile(conn, query, "match_data_all.csv")
    conn.close()

def convertShotData():
    conn = sqlite3.connect("match_data.db")
    query = "SELECT * FROM SpeakerShots"
    convertSQLToCSVFile(conn, query, "shot_data.csv")
    conn.close()

def convertPitData():
    conn = sqlite3.connect("match_data.db")
    query = "SELECT * FROM PitData"
    convertSQLToCSVFile(conn, query, "pit_data.csv")
    conn.close()

def convertCustomSQLQuery(query: str):
    conn = sqlite3.connect("match_data.db")
    convertSQLToCSVFile(conn, query, "match_data.csv")
    conn.close()

def convertSQLToCSVFile(conn: sqlite3.Connection, sql_query: str, output_filename: str):
    cur = conn.execute(sql_query)
    data = cur.fetchall()
    cur.close()
    with open(output_filename, "a+") as f:
        for entry in data:
            csv = ""
            for value in entry:
                csv += f"{value},"
            f.write(csv.removesuffix(",") + "\n")

def pullData() -> bool:
    os.system("./adb -d shell \"run-as org.skylinerobotics.skyscout cat databases/match_data.db\" > match_data.db")
    # file exists and size is greater than 0
    if os.path.exists("match_data.db") and os.path.getsize("match_data.db") > 0:
        return True
    return False

def promptMatchNumber() -> int:
    match = input("Match: ")
    while not match.isnumeric():
        print("enter a valid match number")
        match = input("Match: ")
    return int(match)

def executeCommand(command: int):
    if command == 1:
        match = promptMatchNumber()
        convertDataAfterMatch(match)
    elif command == 2:
        convertAllMatchData()
    elif command == 3:
        convertShotData()
    elif command == 4:
        convertPitData()
    elif command == 5:
        query = input("Enter custom query: ")
        convertCustomSQLQuery(query)


