import os
import sqlite3
import csv

class DatabaseConnector:
    def __init__(self, path):
        self.path = path
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
    
    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

class CSVExporter:
    def __init__(self, path):
        self.path = path

    def export_to_csv(self, data):
        with open(self.path, "a+") as f:
            writer = csv.writer(f)
            writer.writerows(data)

class ConversionCommand:
    def __init__(self, connector: DatabaseConnector, exporter: CSVExporter):
        self.connector = connector
        self.exporter = exporter
        self.query = ""

    def execute(self):
        data = self.connector.execute_query(self.query)
        self.exporter.export_to_csv(data)

class ConvertAllMatchDataCommand(ConversionCommand):
    def __init__(self, connector, exporter):
        super(ConvertAllMatchDataCommand, self).__init__(connector, exporter)
        self.query = "SELECT * FROM MatchData"

class ConvertAfterMatchCommand(ConversionCommand):
    def __init__(self, connector, exporter, match):
        super(ConvertAfterMatchCommand, self).__init__(connector, exporter)
        self.query = f"SELECT * FROM MatchData WHERE MatchNumber > {match}"

class ConvertShotDataCommand(ConversionCommand):
    def __init__(self, connector, exporter):
        super(ConvertShotDataCommand, self).__init__(connector, exporter)
        self.query = f"SELECT * FROM SpeakerShots"

class ConvertPitDataCommand(ConversionCommand):
    def __init__(self, connector, exporter):
        super(ConvertPitDataCommand, self).__init__(connector, exporter)
        self.query = f"SELECT * FROM PitData"


class OptionExecutionHandler:
    def __init__(self):
        self.connector = DatabaseConnector("match_data.db")
    
    def print_options(self):
        print("1) Convert After Match")
        print("2) Convert All Matches")
        print("3) Convert Shot Data")
        print("4) Convert Pit Data")
    
    def start_command_input(self):
        self.print_options()
        while True:
            option = input(">>> ")
            if option == "1":
                match = int(input("Enter match: "))
                self.execute_after_match_command(match)
                break
            elif option == "2":
                self.execute_all_matches_command()
                break
            elif option == "3":
                self.execute_shot_data_command()
                break
            elif option == "4":
                self.execute_pit_data_command()
                break
            else:
                print("Invalid Input.")
    
    def execute_after_match_command(self, match):
        exporter = CSVExporter(f"match_data_after_{match}.csv")
        ConvertAfterMatchCommand(self.connector, exporter, match).execute()

    def execute_all_matches_command(self):
        exporter = CSVExporter(f"match_data_all.csv")
        ConvertAllMatchDataCommand(self.connector, exporter).execute()

    def execute_shot_data_command(self):
        exporter = CSVExporter(f"shot_data.csv")
        ConvertShotDataCommand(self.connector, exporter).execute()
    
    def execute_pit_data_command(self):
        exporter = CSVExporter(f"pit_data.csv")
        ConvertPitDataCommand(self.connector, exporter).execute()
    
    def close_option_executor(self):
        self.connector.disconnect()

class DataRetriever:
    def __init__(self, output_filename):
        self.output_filename = output_filename
    
    def retrieve_data(self):
        os.system(f"./adb -d shell \"run-as org.skylinerobotics.skyscout cat databases/match_data.db\" > {self.output_filename}")
        return self.isSuccessful()

    def isSuccessful(self):
        if os.path.exists(self.output_filename) and os.path.getsize(self.output_filename) > 0:
            return True
        return False

if __name__ == "__main__":
    retriver = DataRetriever("match_data.db")
    if not retriver.retrieve_data():
        print("Data couldn't be retrieved. Check connection.")
        exit(1)

    handler = OptionExecutionHandler()  # Create executor
    handler.start_command_input()       # Start command loop
    handler.close_option_executor()     # Close executor after command loop completes