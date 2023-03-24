import json
import os
from pathlib import Path

from view import *
from model import *
from datetime import datetime


class Controller:
    def __init__(self):
        self.view = View(
            header="----------------------------------------\n| Welcome to Chess Tournament Software "
                   "|\n---------------------------------------- \n",
            footer="\n*Select the commande by typing the number\n",
        )
        self.players = {}  # TODO charger les joueurs au démarrage
        self.tournaments = {}
        self.current_tournament = None

    def display_main_menu(self):
        choices = {
            0: "Manage Players",
            1: "Manage Tournaments",
            2: "Manage the current Tournament",
            3: "Show Reports",
            4: "Load / Save data",
            5: "Exit"
        }

        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            self.display_player_management_menu()
        elif user_choice == "1":
            self.display_tournament_management_menu()
        elif user_choice == "2":
            self.display_current_tournament_management_menu()
        elif user_choice == "3":
            self.display_reports_menu()
        elif user_choice == "4":
            self.display_data_menu()
        elif user_choice == "5":
            self.exit()

        # while user_choice != str(3):  # if user do not want to quite
        #
        #     if user_choice == "0":  # add a new tournament and write to json
        #         new_tournament = View().display_add_new_tournament_menu()
        #         write_to_json(new_tournament)
        #     elif user_choice == "1":
        #         if not os.path.exists('JSON FILES'):
        #             print('**//!!!There is no tournament for the moment!!!//**\n\n\n')
        #             user_choice = View().display_menu()
        #             return user_choice
        #         else:
        #             new_tournaments = load_from_json()
        #             if len(new_tournaments) == 0:  # if there is no json file
        #                 print('**//!!!There is no tournament for the moment!!!//**\n\n\n')
        #                 user_choice = View().display_menu()
        #                 return user_choice
        #             else:
        #                 View().display_current_tournament(check_current_tournament(new_tournaments))
        #                 print(View().__init__().footer)
        #     elif user_choice == "2":
        #         new_tournaments = load_from_json()
        #         View().display_previous_tournament(check_finished_tournament(new_tournaments))
        #     else:
        #         raise ValueError
        #     user_choice = View().display_menu()

    def display_player_management_menu(self):
        choices = {
            0: "Create new Player",
            1: "Update existing Player",
            2: "Show all Players",
            3: "Back",
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            self.create_new_player()
        elif user_choice == "1":
            self.update_player()
        elif user_choice == "2":
            self.display_players()
        elif user_choice == "3":
            self.display_main_menu()


def change_char_to_date(char_date):
    date = datetime.strptime(char_date, "%d/%m/%Y")
    return date


def write_to_json(dict_file):
    filename = dict_file["Name"]
    if not os.path.exists('JSON FILES'):
        os.mkdir('JSON FILES')
    filename = Path('JSON FILES/' + filename + '.json')
    with open(filename, 'w') as json_object:
        json.dump(dict_file, json_object)


def load_from_json():
    filedir = Path(os.getcwd() + '/JSON FILES/')  # read all the json files in the directory
    filenames = os.listdir(filedir)
    tournaments = []
    for filename in filenames:
        filename = Path(os.getcwd() + '/JSON FILES/' + filename)
        with open(filename) as json_object:
            tournaments.append(json.load(json_object))
    return tournaments


def if_match_is_fin(date):
    today = datetime.now().strftime('%d/%m/%Y')
    today = datetime.now().strptime(today, '%d/%m/%Y')
    fin_date_match = datetime.strptime(date, '%d/%m/%Y')
    days = (fin_date_match - today).days
    return days


def list_to_dict(data):
    new_date = {i: value for i, value in enumerate(date)}
    return new_date


def print_list(data, key):  # a list of element dictonary type
    new_list = []
    for i in data:
        new_list.append(i[key])
    new_dict = {i: value for i, value in enumerate(new_list)}
    return new_dict


def check_current_tournament(tournaments):
    list_finished_tournament = []
    list_current_tournament = []
    for tournament in tournaments:  # check the last day of the game is earlier than today
        if if_match_is_fin(tournament["Last match date DD/MM/YYYY"]) > 0:
            list_current_tournament.append(tournament)
    return list_current_tournament


def check_finished_tournament(tournaments):
    list_finished_tournament = []
    for tournament in tournaments:  # check the last day of the game is earlier than today
        if if_match_is_fin(tournament["Last match date DD/MM/YYYY"]) <= 0:
            list_finished_tournament.append(tournament)
    return list_finished_tournament
