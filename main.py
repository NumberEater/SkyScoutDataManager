import sqlite3
import os.path
import os
import pandas as pd

# doPull = input("Pull (y/n): ")
numTablets = int(input("Number of Tablets: "))

for i in range(numTablets):
    input("Press enter for next tablet.")
    filename = f"match_data_{i}.db"
    while True:
        os.system(f"./adb -d shell \"run-as org.skylinerobotics.skyscout cat databases/match_data.db\" > {filename}")
        if not (os.path.exists(filename) and os.path.getsize(filename) > 0):
            input("Pull failed. Check connection. Press enter when ready.")
        else:
            print("Pulled Successfully.")
            break


lastMatch = int(input("Last match uploaded (-1 to get all matches): "))
matchesFrame = pd.DataFrame()
pitFrame = pd.DataFrame()
shotFrame = pd.DataFrame()
for i in range(numTablets):
    filename = f"match_data_{i}.db"
    with sqlite3.connect(filename) as conn:
        matchesFrame = pd.concat([matchesFrame, pd.read_sql_query(f"SELECT * FROM MatchData WHERE MatchNumber > {lastMatch}", conn)], ignore_index=True)
        pitFrame = pd.concat([pitFrame, pd.read_sql_query("SELECT * FROM PitData", conn)], ignore_index=True)
        shotFrame = pd.concat([shotFrame, pd.read_sql_query("SELECT * FROM SpeakerShots", conn)], ignore_index=True)

writer = pd.ExcelWriter("output.xlsx", "openpyxl")

matchesFrame["LeftWing"] = matchesFrame["LeftWing"].astype(bool)
matchesFrame["Park"] = matchesFrame["Park"].astype(bool)
matchesFrame["Onstage"] = matchesFrame["Onstage"].astype(bool)
matchesFrame["Spotlight"] = matchesFrame["Spotlight"].astype(bool)
matchesFrame["Harmony"] = matchesFrame["Harmony"].astype(bool)
matchesFrame["Breakdown"] = matchesFrame["Breakdown"].astype(bool)
matchesFrame.to_excel(writer, "Matches", header=False, index=False)

pitFrame["CanDriveUnderStage"] = pitFrame["CanDriveUnderStage"].astype(bool)
pitFrame["Amp"] = pitFrame["Amp"].astype(bool)
pitFrame["Speaker"] = pitFrame["Speaker"].astype(bool)
pitFrame["Trap"] = pitFrame["Trap"].astype(bool)
pitFrame["GroundIntake"] = pitFrame["GroundIntake"].astype(bool)
pitFrame["SourceIntake"] = pitFrame["SourceIntake"].astype(bool)
pitFrame["Climb"] = pitFrame["Climb"].astype(bool)
pitFrame["CanHarmonize"] = pitFrame["CanHarmonize"].astype(bool)
pitFrame.to_excel(writer, "Pit", header=False, index=False)

shotFrame["Scored"] = shotFrame["Scored"].astype(bool)
shotFrame.to_excel(writer, "Shots", header=False, index=False)

writer.close()