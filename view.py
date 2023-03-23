from model import *
from controller import *
class View():

    def __init__(self):
        self.header = ("----------------------------------------\n| Welcome to Chess Tournament Software |\n--"
                       "-------------------------------------- \n")
        self.header_main = ("*What do you want to do ?\n")
        self.header_add_tournament = ("*Please complete the information below")
        self.footer = ("\n*Select the commande by typing the number\n")


    def display_menu(self):

    #a block to show add a new tournament,after the input return to the main menu

        print(self.header)
        print(self.header_main)
        self.menu = {
            0: "Add a new tournament",
            1: "Manage the current tournament ",
            2: "Show the previous tournament",
            3: "Quite"
        }
        display_dict(self.menu)
        choice = input(self.footer)
        return choice

    def display_add_new_tournament_menu(self):

    #a block to show add a new tournament,after the input return to the main menu

        tournament = Tournament().dict_tournament()        #initialization data
        tournament.pop("List of players participate")      #delete the element "player" handle it separately
        print(self.header)
        print(self.header_add_tournament)
        tournament = update_dict(tournament)
        player = []
        reponse = input("Do you want to add player? Y/N \n")
        while reponse in ["y", "Y"]:
            player = add_players(player)
            reponse = input("Do you want to add player? Y/N \n")
        tournament.update({"List of players participate": player})
        print(display_dict(tournament))
        return tournament

    def display_current_tournament(self,tournaments):
        print(self.header)
        tournament = Tournament()
        for index, tournament in enumerate(tournaments):
            print(f'{index+1} : {tournament["Name"]}')
        choice = input("\n*Select the tournament you want to manage by typing its number \n")
        return choice

    def display_manage_tournament(self):
        print(self.header)
        dict_manage_tournament = {
            0: "Add a new player",
            1: "Generate next match",
            2: "Add the result of last round",
            3: "Show the history results"
        }
        display_dict(dict_manage_tournament)
        choice = input(self.footer)
        return choice

    def display_previous_tournament(self,tournaments):
        print(self.header)
        tournament = Tournament()
        for index, tournament in enumerate(tournaments):
            print(f'{index+1} : {tournament["Name"]}')
        choice = input("\n*Select the tournament you want to manage by typing its number \n")
        return choice

def display_dict(dict):

    #a function that will show the dictionary line by line

    for key, value in dict.items():
        print(f'{key}:{value}')


def update_dict(dict):

    #a function that will update the data after input manipulations by users

    new_dict = {}
    for key, value in dict.items():
        value = str(input(f'Please enter the {key}\n'))
        key = key
        new_dict.update({key: value})
    return new_dict


def add_players(listplayer):

#a function that will update a list of players after input manipulations by users

    player = Player().dict_player()
    if listplayer is None:
        listplayer = []
        listplayer.append(update_dict(player))
    else :
        listplayer.append(update_dict(player))
    return listplayer
