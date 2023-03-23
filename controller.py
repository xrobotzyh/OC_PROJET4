import json
import os
from pathlib import Path

from view import *
from model import *
from datetime import datetime


class Controller_display_menu():
    def __init__(self):
        pass

    def manage_menu(self):

        self.choice = View().display_menu()                   # show the main menu
        while self.choice != str(3):                          # if user do not want to quite
            if self.choice == "0":                            # add a new tournament and write to json
                new_tournament = View().display_add_new_tournament_menu()
                write_to_json(new_tournament)
            elif self.choice == "1":
                filedir = Path(os.getcwd()+'/JSON FILES/')    # read all the json files in the directory
                filenames = os.listdir(filedir)
                list_current_tournament = []
                list_finished_tournament = []
                if filenames == None :                        # if there is no json file
                    print('**//!!!There is no tournament for the moment!!!//**\n\n\n')
                    self.choice = View().display_menu()
                    return self.choice
                else :
                    for filename in filenames:                # check the last day of the game is earlier than today
                        new_tournament = load_from_json(filename)
                        if if_match_is_fin(new_tournament["Last match date DD/MM/YYYY"]) <= 0:
                            list_finished_tournament.append(new_tournament)
                        else :
                            list_current_tournament.append(new_tournament)
                            display_dict(print_list(list_current_tournament,"Name"))
                self.choice = input("Which one would you like to manage ? \n")
                print(self.footer)
                #self.choice = View().display_manage_tournament()
            elif self.choice == "2":
                display_dict(print_list(list_finished_tournament,"Name"))
            else:
                raise ValueError
            self.choice = View().display_menu()
        return print("See you next time.")


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


def load_from_json(filename):
    filename = Path('JSON FILES/' + filename)
    with open(filename) as json_object:
        dict = json.load(json_object)
    return dict


def if_match_is_fin(date):
    today = datetime.now().strftime('%d/%m/%Y')
    today = datetime.now().strptime(today, '%d/%m/%Y')
    fin_date_match = datetime.strptime(date, '%d/%m/%Y')
    days = (fin_date_match - today).days
    return days

def list_to_dict(data):
    new_date = {i:value for i,value in enumerate(date)}
    return new_date

def print_list(data,key): #a list of element dictonary type
    new_list = []
    for i in data:
        new_list.append(i[key])
    new_dict = {i:value for i,value in enumerate(new_list)}
    return new_dict