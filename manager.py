import sqlite3
import os
import os.path

os.system("./adb -d shell \"run-as org.skylinerobotics.skyscout cat databases/match_data.db\" > match_data.db")

with sqlite3.connect("match_data.db") as conn:
    cur = conn.execute("SELECT * FROM ScoutData")

    scoutData = cur.fetchall()
    with open("match_data.csv", "a+") as f:
        for match in scoutData:
            csv = ""
            for datapoint in match:
                csv += f"{datapoint},"
            csv = csv.removesuffix(",")
            f.write(csv + "\n")
    
    cur.execute("SELECT * FROM SpeakerShots")
    shotData = cur.fetchall()
    with open("shot_data.csv", "a+") as f:
        for shot in shotData:
            csv = ""
            for dataPoint in shot:
                csv += f"{dataPoint},"
            csv = csv.removesuffix(",")
            f.write(csv + "\n")
    
    cur.execute("SELECT * FROM PitData")
    pitData = cur.fetchall()
    with open("pit_data.csv", "a+") as f:
        for pitScout in pitData:
            csv = ""
            for dataPoint in pitScout:
                csv += f"{dataPoint},"
            csv = csv.removesuffix(",")
            f.write(csv + "\n")
