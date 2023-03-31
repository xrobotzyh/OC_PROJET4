import json
import os
import random
from pathlib import Path

from datetime import datetime
from typing import Dict, Any

from view import View
from model import *


class Controller():
    def __init__(self):

        self.view = View(
            header="----------------------------------------\n| Welcome to Chess Tournament Software "
                   "|\n---------------------------------------- \n",
            footer="\n*Select the commande by typing the number\n",
        )
        self.players = self.load_players_from_json()
        self.tournaments = {}
        self.current_tournament = None

    def load_players_from_json(self) -> Dict[int, Player]:
        json_players_list = load_json_file('players.json')
        players = {}
        for json_player in json_players_list:
            player = Player.from_values(json_player)
            players[player.id] = player
        return players

    def load_tournaments_from_json(self) -> Dict[int, Tournament]:
        # TODO
        return {}

    def display_main_menu(self):
        choices = {
            "0": "Manage Players",
            "1": "Manage tournament",
            "2": "Show Reports",
            "3": "Load/Sava data",
            "4": "Exit"
        }

        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            self.display_player_management_menu()
        elif user_choice == "1":
            self.view.display_tournament_manage_menu()
        elif user_choice == "2":
            self.view.display_current_tournament_management_menu()
        elif user_choice == "3":
            self.view.display_show_rapports_memu()
        elif user_choice == "4":
            self.view.display_data_menu()
        elif user_choice == "5":
            self.view.display_message("\nSee you next time !\n")
            exit(0)

    def display_player_management_menu(self):
        choices = {
            "0": "Create a new Player",
            "1": "Update an existing Player",
            "2": "Show all Players",
            "3": "Back",
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

    def create_new_player(self):
        input_fields = Player.INPUT_FIELDS
        user_inputs = self.view.get_user_inputs(input_fields)
        user_inputs['id'] = str(self.generate_user_id())
        player = Player.from_values(user_inputs)
        self.players[player.id] = player
        self.persist_players()

        self.view.display_message(f'Player {player.first_name} {player.last_name} added with id={player.id}\n')
        self.display_player_management_menu()

    def persist_players(self):
        # TODO
        pass

    def generate_user_id(self) -> int:
        # Generate a new user_id that is not already in the database
        # WARNING: to make sure we don't override other players, we need to load the
        # players database before adding a new player
        user_id = len(self.players) + 1
        while user_id in self.players.keys():
            user_id = user_id + 1
        return user_id

    def create_a_new_dict(self, listdata: list, new_data: dict):
        # a function that will update a list of players after input manipulations by users
        if listdata is None:
            listdata = []
        listdata.append(update_dicts(new_data))
        return listdata

    def write_to_json_dictionary(self, dict_file):
        filename = dict_file["Name"]
        if not os.path.exists('resources'):
            os.mkdir('resources')
        filename = Path('resources/' + filename + '.json')
        with open(filename, 'w') as json_object:
            json.dump(dict_file, json_object)

    def write_to_json_list(self, filename, list_file):
        if not os.path.exists('resources'):
            os.mkdir('resources')
        filename = Path('resources/' + filename + '.json')
        with open(filename, 'w') as json_object:
            for single_element in list_file:
                json.dump(single_element, json_object)

    def display_players(self):
        self.view.display_message("### Players List ###")
        for player_id, player in self.players.items():
            player_msg = ""
            for field, value in player.as_dict().items():
                player_msg += f"{field}: {value}, "
            self.view.display_message(player_msg)
        self.display_player_management_menu()


def parse_date(str_date: str) -> datetime:
    date = datetime.strptime(str_date, "%d/%m/%Y")
    return date


def load_from_json():
    filedir = Path(os.getcwd() + '/resources/')  # read all the json files in the directory
    filenames = os.listdir(filedir)
    tournaments = []
    for filename in filenames:
        filename = Path(os.getcwd() + '/resources/' + filename)
        with open(filename) as json_object:
            tournaments.append(json.load(json_object))
    return tournaments


# def if_match_is_fin(date):
#     today = datetime.now().strftime('%d/%m/%Y')
#     today = datetime.now().strptime(today, '%d/%m/%Y')
#     fin_date_match = datetime.strptime(date, '%d/%m/%Y')
#     days = (fin_date_match - today).days
#     return days

def load_json_file(filename):
    filename = Path(os.getcwd() + '/resources/' + filename)
    with open(filename) as json_file:
        json_values = json.load(json_file)
    return json_values


def list_to_dict(data):
    new_date = {i: value for i, value in enumerate(date)}
    return new_date


def print_list(data, key):  # a list of element dictonary type
    new_list = []
    for i in data:
        new_list.append(i[key])
    new_dict = {i: value for i, value in enumerate(new_list)}
    return new_dict


def list_of_current_tournament(tournaments):
    list_current_tournament = []
    for tournament in tournaments:  # check the last day of the game is earlier than today
        if if_match_is_fin(tournament["Last match date DD/MM/YYYY"]) > 0:
            list_current_tournament.append(tournament)
    return list_current_tournament


def list_of_finished_tournament(tournaments):
    list_finished_tournament = []
    for tournament in tournaments:  # check the last day of the game is earlier than today
        if if_match_is_fin(tournament["Last match date DD/MM/YYYY"]) <= 0:
            list_finished_tournament.append(tournament)
    return list_finished_tournament


def create_a_new_dict(listdata: list, new_data: dict):
    # a function that will update a list of players after input manipulations by users
    if listdata is None:
        listdata = []
    listdata.append(update_dicts(new_data))
    return listdata


def update_one_dict(dictid: str, listdata: list, key: str):
    is_in = False
    for i, data in enumerate(listdata):
        if player[key] == dictid:
            listdata[i] = update_dicts(player)
            is_in = True
    if is_in == False:
        print(f"There is no such {dictid}")
    return listdata


def generate_random_opponent_first_match(list_contestants):
    """
    for the first round game,we use random function
    :param list_contestants: a list of contestants for the tournaments
    :return: a dictionary key = round information value = list every opponents
    """
    random.shuffle(list_contestants)
    if (len(list_contestants)) % 2 == 0:
        list_temporary = [list_contestants[i:i + 2] for i in range(0, len(list_contestants), 2)]
        list_player_opponent_round = {1: list_temporary}
        return list_player_opponent_round
    else:
        list_temporary = [list_contestants[i:i + 2] for i in range(0, len(list_contestants) - 1, 2)]
        list_temporary.append([list_contestants[-1], None])
        list_player_opponent_round = {"1": list_temporary}
        return list_player_opponent_round


def display_enter_winner(players_opponent):
    winner = input(f'Please enter the winner of the game {players_opponent[0]} vs '
                   f'{players_opponent[1]}. '
                   f'The winner is 1 or 2 or 0 for Draw\n')
    return winner


def update_winner_state_match(list_opponent_in_match, rounds):
    """
    :param list_opponent_in_match: a list contains [every opponents information] in a round
    :param rounds: round number
    :return: a list contain two list,list one[opponents information],two [winner],list_opponent_in_match is a dict
             contains round number and list player in match with winner
    """
    list_player_in_match_with_winner = []
    for players_opponent in list_opponent_in_match[rounds]:
        winner = display_enter_winner(players_opponent)
        players_opponent.append(winner)
        list_temporary = [players_opponent[i:i + 2] for i in range(0, len(players_opponent), 2)]
        list_player_in_match_with_winner.append(list_temporary)
    list_opponent_in_match[rounds] = list_player_in_match_with_winner
    return list_player_in_match_with_winner, list_opponent_in_match


def update_scores_after_match(list_player_in_match_with_winner, list_player_with_score):
    """
    update a list player with scores of every player by using another element [0],[1],[2] in list player in match with
    winner
    :param list_player_in_match_with_winner: list opponent with another element winner information
    :param list_player_with_score: list of total players with theirs scores
    :return: list of total players with theirs scores
    """
    i = 0
    while i < len(list_player_in_match_with_winner):
        if list_player_in_match_with_winner[i][1] == list("0"):
            for player_with_score in list_player_with_score:
                if player_with_score["player :"] == list_player_in_match_with_winner[i][0][0]:
                    score = player_with_score["score :"]
                    score += 0.5
                    player_with_score.update({"player :": list_player_in_match_with_winner[i][0][0], "score :": score})
                elif player_with_score["player :"] == list_player_in_match_with_winner[i][0][1]:
                    score = player_with_score["score :"]
                    score += 0.5
                    player_with_score.update({"player :": list_player_in_match_with_winner[i][0][1], "score :": score})
        elif list_player_in_match_with_winner[i][1] == list("1"):
            for player_with_score in list_player_with_score:
                if player_with_score["player :"] == list_player_in_match_with_winner[i][0][0]:
                    score = player_with_score["score :"]
                    score += 1
                    player_with_score.update({"score :": score})
        else:
            for player_with_score in list_player_with_score:
                if player_with_score["player :"] == list_player_in_match_with_winner[i][0][1]:
                    score = player_with_score["score :"]
                    score += 1
                    player_with_score.update({"score :": score})

        i += 1
    return list_player_with_score  # return a list with [{player:A,score:int},{},{}]


def sort_list_of_players_by_scores(list_player_with_score):
    list_player_sorted_by_scores = sorted(list_player_with_score, key=lambda player_with_score:
    player_with_score.__getitem__("score :"), reverse=True)
    return list_player_sorted_by_scores


def generate_next_round_match(list_player_with_score):
    list_player_next_round = []
    for player_with_score in list_player_with_score:
        list_player_next_round.append(player_with_score["player :"])  # a list without scores informations but sorted
