"""

Competition program
~~~~~~~~~~~~~~~~~~~

A program to enter data and output data for any event

"""

__title__ = "Competition program"
__author__ = "BSpoones"
__version__ = "1.0.0"
__copyright__ = "Copyright 2021-2026"

import json,re
import sqlite3
from time import sleep
from sqlite3 import connect



class Competiton:
    """Competition object containing all functions to run a competition"""
    def __init__(self):
        # Variables below used for presence checks only, these are newly assigned in enter_competitors()
        self.teams = {}
        self.individuals = {}
        self.events = []
    
    def event_choice(self):
        self.events = (input("Please enter each event you would like to include, seperated by commas (,): ").split(",")) # Creates list of events from input
        self.events = list(map(lambda x: x.lstrip(),self.events)) # Removes leading space that may occour when entering information
        if any(item=="" for item in self.events): # Prevents blank events
            print("One or more of the events is blank")
            return self.event_choice()
        nl = "\n" # Newline character in variable because python struggles with backslashes in f strings
        confirmation = input(f"Your selected events are:\n{nl.join(self.events)}\nAre you happy with your selection (Y/N)") # Shows formatted list of entered events for confirmation
        if confirmation.lower() in ("y","yes"): # Using .lower() to avoid checking for caps, allows for a smaller check
            pass
        elif confirmation.lower() in ("n","no"):
            return self.event_choice()
        else:
            print("Please select a valid confirmation")
            return self.event_choice()
    
    def team_input(self):
        team = {} # Blank dict to be filled and appended to self.teams
        team_name = input("Please enter a team name: ")
        if team_name in self.teams.keys() or team_name in self.individuals.keys(): # Checks both dicts to avoid duplicate entries in event_scores
            print("This team name is already in use")
            return self.team_input()
        team_members = input("Please enter the names of each member, seperated by a comma (,): ").split(",") # Creates list of members from input
        team_members = list(map(lambda x: x.lstrip(), team_members)) # Removes leading space that may occour when entering information
        for name in team_members:
            if not self.name_validation(name): # If it fails the name validation
                print(f"{name} is an invalid team name, please try again")
                return self.team_input()
        team["members"] = team_members
        team["positions"] = []
        team["scores"] = []
        self.teams[team_name] = team # Final output = {TEAMNAME: {members:[Name1,Name2,Name3],events:[4,3,2,2,5]}}
    
    def individual_input(self):
        individual = input("Please enter the name for the individual: ")
        if individual in self.individuals.keys() or individual in self.teams.keys():  # Checks both dicts to avoid duplicate entries in event_scores
            print("This name is already in use")
            return self.individual_input()
        if not self.name_validation(individual): # If it fails name validation
            print("This is an invalid name, please ensure you have spelled it correctly.")
            return self.individual_input()
        self.individuals[individual] = {"positions":[], "scores": []} # Empty lists used later as a presence check for showing scores
        # Final output = {INDIVIDUAL_NAME: []}
    
    def name_validation(self, name):
        if name is None or not re.fullmatch('[A-z]{2,25}( [A-z]{2,25})?',name): # Presence and Regex check for either 1 or 2 words containing only letters between 2 and 25 characters each
            return False
        else:
            return True
    
    def enter_scores(self):
        print("Teams:")
        for team_name in self.teams.keys(): # Team names stored as keys in dict
            print(f"{team_name}")            
        print("Individuals:")
        for individual_name in self.individuals.keys(): # Individual names stored as keys in dict
            print(f"{individual_name}")
        competitor = input("Please select a competitor from the list below: ")
        if competitor in self.teams.keys():
            competitor_item = self.teams[competitor] # Easier way to search for competitor data than a for loop, competitor_item var still changes dict item
        elif competitor in self.individuals.keys():
            competitor_item = self.individuals[competitor] # Easier way to search for competitor data than a for loop, competitor_item var still changes dict item
        else:
            print("Competitor not found, please ensure you have typed it properly")
            return self.enter_scores()
        
        if competitor_item["positions"] != []: # If the user has already entered scores, they appear
            scores_list = competitor_item["positions"]
            print("Current scores:")
            for i, event in enumerate(self.events):
                print(f"{event:<10}{scores_list[i]}") # Outputs formatted event scores
        else:
            # If nothing has been input, it just shows the scores
            print("Events:")
            for event in self.events:
                print(event)
        new_positions = input("Please enter your new positions for every event, seperated by a comma (,)").split(",") # Splits input into list
        try:
            new_positions = [int(x) for x in new_positions] # Sets every item from input to be an int
        except:
            print("One or more items in the string was not a number")
            return self.enter_scores()
        if len(new_positions) != len(self.events): # Checks if input matches the amount of events
            print("You have entered too few or too many positions.")
            return self.enter_scores()
        for i, event in enumerate(self.events):
            print(f"{event:<10}{new_positions[i]}") # Outputs events and the selected score
        confirmation = input(f"Are you happy with your selection (Y/N)")
        if confirmation.lower() in ("y","yes"):
            pass
        elif confirmation.lower() in ("n","no"):
            return self.enter_scores()
        else:
            print("Please select a valid confirmation")
            return self.enter_scores()
        
        new_scores = []
        total_participants = len(self.teams.keys()) + len(self.individuals.keys()) # Sums the length of all competitors
        for position in new_positions:
            # Formula to calculate scores: score = total_participants - position + 1
            score = total_participants - position + 1
            new_scores.append(score)
        competitor_item["scores"] = new_scores
        competitor_item["positions"] = new_positions
    
    def enter_new_data(self):
        # Resets data if already entered
        self.teams = {}
        self.individuals = {}
        self.events = []   
        self.event_choice()
        while True: # Keeps showing menu until user selects finished
            if self.enter_competitors():
                break
        while True: # Keeps showing menu until user selects finished
            if self.enter_scores_menu():
                break
        
    def enter_competitors(self):
        print("Please enter all teams and indaviduals by selecting one of the following\n\n[1] Enter a team\n[2] Enter an indavidual\n[3] I've entered all competitors")
        selection = input("Please enter your choice: ")
        if selection == '1':
            self.team_input()
        elif selection == '2':
            self.individual_input()
        elif selection == '3':
            if self.teams == {} and self.indaviduals == {}: # Checks if both lists are empty (No data entered)
                print("You need at least one competitor")
                return False
            else:
                return True
        else:
            print("Please select a valid input")
            return self.enter_competitors()
        
    def enter_scores_menu(self) -> str:
        print("Please enter all teams and indaviduals by selecting one of the following\n\n[1] Enter a score\n[2] I've entered all competitors")
        selection = input("Please enter your choice: ")
        if selection == '1':
            self.enter_scores()
        elif selection == '2':
            return True
    
    def output_menu(self) -> str:
        print("Please select a method to show the data:\n\n[1] Show podium\n[2] Show all scores\n[3] Show team scores\n[4] Show individual scores\n[5] Show scores for event")
        selection = input("\nPlease enter your choice:")
        if selection == '1':
            self.show_podium()
        elif selection == "2":
            self.show_all_scores()
        elif selection == "3":
            self.team_scores()
        elif selection == "4":
            self.individual_scores()
        elif selection == "5":
            self.event_scores()
        else:
            print("Please select a valid input")
            sleep(1)
            return self.output_menu()

    def import_menu(self) -> str:
        print("Please select one of the following:\n\n[1] Import from JSON\n[2] Import from database")
        selection = input("\nPlease enter your choice: ")
        if selection == "1":
            self.load_from_JSON()
        elif selection == "2":
            self.load_from_db()
        else:
            print("Please select a valid input")
            return self.import_menu()
    
    def export_menu(self) -> str:
        print("Please select one of the following:\n\n[1] Export to JSON\n[2] Export to database")
        selection = input("\nPlease enter your choice: ")
        if selection == "1":
            self.save_to_JSON()
        elif selection == "2":
            self.save_to_db()
        else:
            print("Please select a valid input")
            return self.export_menu()
    
    def show_podium(self) -> str:
        final_scores = {}
        for key, val in self.teams.items(): # Iterates through every item in self.teams
            team_name = key
            total_score = sum(val["scores"]) # Sums every item in scores list to get total score
            final_scores[team_name] = total_score
        for key, val in self.individuals.items(): # Iterates through every item in self.individuals
            name = key
            total_score = sum(val["scores"]) # Sums every item in scores list to get total score
            final_scores[name] = total_score
        sorted_final_scores = dict(sorted(final_scores.items(), key=lambda item: item[1],reverse=True)) # Sorts dict so position values can be used for top 3
        final_score_key = [*sorted_final_scores] # Python method to get list of keys of dict
        final_score_values = [*sorted_final_scores.values()] # Python method to get list of values of dict
        if len(sorted_final_scores) < 3:
            print("Final scores")
            for key,value in sorted_final_scores.items():
                print(f"{key:<10}{value}") # Outputs data
        else:
            # No for loop is used as there are only 3 values
            print("Podium:\n")
            print(f"First place: {final_score_key[0]} with {final_score_values[0]}")
            print(f"Second place: {final_score_key[1]} with {final_score_values[1]}")
            print(f"Third place:{final_score_key[2]} with {final_score_values[2]}")
            print("") # New line to seperate output later
    
    def show_all_scores(self) -> str:
        final_scores = {}
        # For loops iterate through every competitor appending their name and total score
        for key, val in self.teams.items():
            team_name = key
            total_score = sum(val["scores"])
            final_scores[team_name] = total_score
        for key, val in self.individuals.items():
            name = key
            total_score = sum(val["scores"])
            final_scores[name] = total_score
        sorted_final_scores = dict(sorted(final_scores.items(), key=lambda item: item[1],reverse=True)) # Sorts dict to be used for rankings
        print("Ranking     Competitor  Score\n")
        for i,(key,val) in enumerate(sorted_final_scores.items()): # Outputs position, name and final score
            print(f"{i+1:<12}{key:<12}{val:<12}")
    
    def team_scores(self) -> str:
        final_scores = {}
        for key, val in self.teams.items(): # Gets all data from teams
            team_name = key
            total_score = sum(val["scores"])
            final_scores[team_name] = total_score
        sorted_final_scores = dict(sorted(final_scores.items(), key=lambda item: item[1],reverse=True)) # Sorts dict to show top scores
        print("Ranking     Competitor  Score\n")
        for i,(key,val) in enumerate(sorted_final_scores.items()): # Outputs ranking, name and total score
            print(f"{i+1:<12}{key:<12}{val:<12}")
    
    def individual_scores(self) -> str:
        final_scores = {}
        for key, val in self.individuals.items(): # Gets all data from individuals
            name = key
            total_score = sum(val["scores"])
            final_scores[name] = total_score
        sorted_final_scores = dict(sorted(final_scores.items(), key=lambda item: item[1],reverse=True)) # Sorts dict to show top scores
        print("Ranking     Competitor  Score\n")
        for i,(key,val) in enumerate(sorted_final_scores.items()): # Outputs ranking, name and total score
            print(f"{i+1:<12}{key:<12}{val:<12}")
    
    def event_scores(self) -> str:
        print("Events:")
        # Input selects event from events list
        for event in self.events:
            print(event)
        event_choice = input("Please choose an event")
        try:
            event_index = self.events.index(event_choice) # Used to edit scores list
        except:
            print("Event not found, please try again")
            return self.event_scores()
        final_scores = {}
        for key, val in self.teams.items(): # Iterates through all values
            team_name = key
            try:
                score = (val["scores"][event_index])
            except:
                score = 0
            print(score)
            final_scores[team_name] = score
        for key, val in self.individuals.items(): # Iterates through all values
            name = key
            try:
                score = (val["scores"][event_index])
            except:
                score = 0
            final_scores[name] = score
        sorted_final_scores = dict(sorted(final_scores.items(), key=lambda item: item[1],reverse=True)) # Sorts dict to show top ranking
        print(f"Scores for {event_choice}:")
        print("Ranking     Competitor  Score\n")
        for i,(key,val) in enumerate(sorted_final_scores.items()): # Outputs ranking, nane and score
            print(f"{i+1:<12}{key:<12}{val:<12}")
        
    def save_to_JSON(self) -> json:
        data = {}
        data["events"] = self.events
        data["teams"] = self.teams
        data["individuals"] = self.individuals
        json.dump(data,open("data.json","w+"),indent=4) # Dumps data dict to JSON file. "w+" creates a file if not present
    
    def load_from_JSON(self) -> json:
        try:
            with open("data.json","r") as f:
                content = json.load(f)
                self.events = content["events"]
                self.teams = content["teams"]
                self.individuals = content["individuals"]
            print("JSON data loaded")
            sleep(1)
        except: # If json doesn't exist or json is empty
            print("Data not found")
            return self.import_menu() # Returns back to choice of imports
    
    def save_to_db(self) -> sqlite3:
        self.cxn = connect("database.db", check_same_thread=False) # Opens database file
        self.cur = self.cxn.cursor() # Sets cursor from SQlite3
        self.cur.execute("DROP TABLE IF EXISTS events") # Deletes table if it already exists, clearing past data
        self.cur.execute("DROP TABLE IF EXISTS teams")
        self.cur.execute("DROP TABLE IF EXISTS individuals")
        event_table = """
        CREATE TABLE events(
            EventName text
        )""" # SQL to create events table
        individual_table = """
        CREATE TABLE individuals (
            IndividualName text,
            IndividualPositions text,
            IndividualScores text
        )"""# SQL to create individuals table
        team_table = """
        CREATE TABLE teams (
            TeamName text,
            TeamMembers text,
            TeamPositions text,
            TeamScores text
        )"""# SQL to create teams table
        self.cur.execute(event_table) # Runs SQL code from above, in seperate lines because SQlite3 can only execute one at a time
        self.cur.execute(team_table)
        self.cur.execute(individual_table)

        for event in self.events:
            self.cur.execute("INSERT INTO events(EventName) VALUES (?)",(event,)) # Adds each event to db table
        for key,value in self.teams.items(): # Iterating through all team data
            team_name = key
            team_members = " ".join(value["members"]) # Using a string as a list because SQlite3 doesn't support lists
            positions = list(map(str, value["positions"])) # Converting to string as SQlite3 doesn't support int
            team_positions = " ".join(positions)
            scores = list(map(str, value["scores"]))
            team_scores = " ".join(scores)
            # Code below adds all team data as a row in database
            self.cur.execute("INSERT INTO teams(TeamName,TeamMembers,TeamPositions,TeamScores) VALUES (?,?,?,?)",(team_name,team_members,team_positions,team_scores))
        for key,value in self.individuals.items(): # Iterating through all individual data
            name = key
            positions = list(map(str, value["positions"])) # Converting to string as SQlite3 doesn't support int
            positions = " ".join(positions) # Using a string as a list because SQlite3 doesn't support lists
            scores = list(map(str, value["scores"]))
            scores = " ".join(scores)
            # Code below adds all individual data as a row in database
            self.cur.execute("INSERT INTO individuals(IndividualName,IndividualPositions,IndividualScores) VALUES (?,?,?)",(name,positions,scores))
        self.cxn.commit() # Commits (saves) all data back to the db
    
    def load_from_db(self):
        try:
            self.cxn = connect("database.db", check_same_thread=False) # Connects to database file
            self.cur = self.cxn.cursor() # Sets database cursor

            self.cur.execute("SELECT EventName FROM events") # Selects all event names from events table
            events = self.cur.fetchall() # Creates a list of tuples
            for item in events: # Iterates through all tuples
                self.events.append(item[0]) # SQlite3 retrieves data as a single length tuple (data,) so the first element is used

            self.cur.execute("SELECT * FROM teams") # Selects everything from teams table
            team_list = self.cur.fetchall() # Creates a list of tuples from each row
            for item in team_list:
                team = {}
                team_name = item[0]
                team_members = item[1].split() # Splits member string into list by a space
                team_positions = item[2].split()
                team_positions = list(map(int,team_positions)) # Converts back to integers
                team_scores = item[3].split()
                team_scores = list(map(int,team_scores))
                team["members"] = team_members
                team["positions"] = team_positions
                team["scores"] = team_scores
                self.teams[team_name] = team # Appends team dict back to self.teams

            self.cur.execute("SELECT * FROM individuals") # Selects everything from individuals table
            team_list = self.cur.fetchall() # Creates a list of tuples from each row
            for item in team_list:
                individual = {}
                name = item[0]
                positions = item[1].split() # Splits string into list by space
                positions = list(map(int,positions)) # Converts back into int for calculations
                scores = item[2].split()
                scores = list(map(int,scores))
                individual["positions"] = positions
                individual["scores"] = scores
                self.individuals[name] = individual # Appends data back to self.individuals
            print("Database data loaded")
            sleep(1)
        except:
            print("Failed to retrieve data")
            return self.import_menu()

def run_competition(): # Run competition outisde of class, this is called when running the code providing a UI for the user
    competition = Competiton() # Creates instance of Competition class
    print("-------------------------------\n\nWelcome to the competition menu\n\n-------------------------------\n")
    print("Please select an option to begin\n[1] Enter new data\n[2] Import data from file\n[3] Exit")
    selection = input("\nPlease enter your choice: ")
    if selection == "1":
        competition.enter_new_data()
    elif selection == "2":
        competition.import_menu()
    elif selection == "3":
        print("The program will now close: ")
        sleep(2)
        exit()
    while True:
        print("Please select one of the following:\n[1] Enter new data\n[2] Export data\n[3] Show results\n[4] Exit")
        selection = input("Please enter your choice: ")
        if selection == "1":
            competition.enter_new_data()
        elif selection == "2":
            competition.export_menu()
        elif selection == "3":
            competition.output_menu()
        elif selection == "4":
            print("The program will now close")
            sleep(2)
            exit()

if __name__ == "__main__": # If this code is being run directly instead of being imported to external project
    run_competition()
