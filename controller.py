import os
from pathlib import Path
from typing import Dict, Optional, List
import random

from tinydb.table import Document

from view import View
from model import Player, Tournament, Match,Round
from tinydb import TinyDB, Query, table
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer
from datetime import datetime


class Controller:


    def __init__(self):

        self.view = View(
            header="----------------------------------------\n| Welcome to Chess Tournament Software "
                   "|\n---------------------------------------- \n",
            footer="\n*Select the commande by typing the number\n",
        )
        # self.tournaments: Dict[int, Tournament] = {}  # self.load_tournaments_from_db()
        self.current_tournament: Optional[Tournament] = None  # self.load_current_tournament_from_db()
        self.db_passed_tournament: Optional[Tournament] = None
        self.db_players = self.reserialization_directory_resources('players')
        self.db_current_tournament = self.reserialization_directory_resources('/data/current_tournament')
        self.db_passed_tournament= self.reserialization_directory_resources('/data/passed_tournament')
        self.players: Dict[int, Player] = self.load_players_from_db()
        # self.tournaments : Dict[int, Tournament] = self.load_tournaments_from_db()
        self.current_tournament : Dict[int,Tournament] = self.load_current_tournaments_from_db()
        self.passed_tournament : Dict[int,Tournament] = self.load_passed_tournaments_from_db()
        self.db_round = self.reserialization_directory_resources('/data/round')
        self.round = self.load_round_from_db()

    def load_players_from_db(self) -> Dict[int, Player]:
        db = self.db_players.all()
        players_documents: List[Document] = db
        players = {}
        for player_document in players_documents:
            players[player_document.doc_id] = Player.from_db(player_document)
        return players

    # def load_tournaments_from_db(self) -> Dict[int,Tournament]:
    #     db = self.db_current_tournament
    #     table_names = db.tables()
    #     tournaments = {}
    #     for table_name in table_names:
    #         tournaments_document = db.table(table_name).all()
    #         for tournament_document in tournaments_document :
    #             tournaments[tournament_document.doc_id] = Tournament.from_db(tournament_document)
    #     return tournaments
    def load_round_from_db(self) -> dict[int,round]:
        db = self.db_round.all()
        round_documents: List[Document] = db
        rounds = {}
        for round_document in round_documents:
            rounds[round_document.doc_id] = Round.from_db(player_document)
        return rounds


    def find_round_by_name(self):
        pass
    def load_current_tournaments_from_db(self):
        db = self.db_current_tournament
        # table_names = db.tables()
        tournaments_document = db.all()
        tournaments = {}
        # for table_name in table_names:
        #     tournaments_document = db.table(table_name).all()
        for tournament_document in tournaments_document:
            tournaments[tournament_document.doc_id] = Tournament.from_db(tournament_document)
        return tournaments

    def load_passed_tournaments_from_db(self):
        db = self.db_passed_tournament
        # table_names = db.tables()
        tournaments_document = db.all()
        tournaments = {}
        # for table_name in table_names:
        #     tournaments_document = db.table(table_name).all()
        for tournament_document in tournaments_document:
            tournaments[tournament_document.doc_id] = Tournament.from_db(tournament_document)
        return tournaments
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
            self.display_tournament_management_menu()
        elif user_choice == "2":
            self.view.display_current_tournament_management_menu()
        elif user_choice == "3":
            self.load_save()
        elif user_choice == "4":
            self.view.display_message("\nSee you next time !\n")
            exit(0)


    def load_save(self):
        self.__init__()
        self.display_main_menu()

    def display_player_management_menu(self):
        choices = {
            "0": "Create a new Player",
            "1": "Update a existing Player",
            "2": "Show all Players",
            "3": "Back",
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            self.create_new_player()
        elif user_choice == "1":
            self.display_update_player_menu()
        elif user_choice == "2":
            self.display_players()
        elif user_choice == "3":
            self.display_main_menu()

    def display_update_player_information_menu(self) ->str :
        choices = {
            "0": "Edit the player's first name",
            "1": "Edit the player's last name",
            "2": "Edit the player's birthday",
            "3": "Edit the player's club id",
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            value = 'first name'
            return value
        elif user_choice == "1":
            value = 'last name'
            return value
        elif user_choice == "2":
            value = 'birthday DD/MM/YYYY'
            return value
        elif user_choice == "3":
            value = 'club id'
            return value


    def display_update_tournament_information_menu(self) ->str :
        choices = {
            "0": "Edit the tournament's name",
            "1": "Edit the tournament's location",
            "2": "Edit the tournament's start date",
            "3": "Edit the tournament's end date",
            "4": "Edit the tournament's total round",
            "5": "Edit the tournament's players list",
            "6": "Edit the tournament's description",
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            value = 'Name'
            return value
        elif user_choice == "1":
            value = 'Location'
            return value
        elif user_choice == "2":
            value = 'First match date DD/MM/YYYY'
            return value
        elif user_choice == "3":
            value = 'Last match date DD/MM/YYYY'
            return value
        elif user_choice == "4":
            value = 'Total number of round'
            return value
        elif user_choice == "5":
            value = 'List of players participate'
            return value
        elif user_choice == "6":
            value = 'Descrition of the tournament'
            return value
        # else :
        #     self.view.display_message('Please entre the number 1-6')


    def create_new_player(self):
        # Create player from user inputs
        input_fields = Player.INPUT_FIELDS
        user_inputs = self.view.get_user_inputs(input_fields)
        user_inputs['id'] = self.generate_user_id()
        player = Player.from_values(user_inputs)

        # Persist player in DB
        db = self.db_players
        player_id = db.insert(Player.as_dict(player))
        player.id = player_id

        self.display_player_management_menu()

    def update_player_by_id(self):
        db = self.db_players
        find_id = input("\n### Enter the id ###\n")
        player = self.players.get(int(find_id))
        if player:
            change_value = self.display_update_player_information_menu()
            new_value = input(f'please enter the new {change_value}\n')
            db.update({change_value:new_value}, doc_ids=[player.id])
            print("Player updated successfully!")
        else:
            print(f"No such a player")
        self.display_player_management_menu()


    def display_update_player_menu(self):
        choices = {
            "0": "Enter player's id to update information",
            "1": "Enter player's first name to find his id",
            "2": "Enter player's last name to find his id",
            "3": "back"
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            self.update_player_by_id()
        elif user_choice == "1":
            self.find_player_id_by_first_name()
        elif user_choice == "2":
            self.find_player_id_by_last_name()
        elif user_choice == "3":
            self.display_player_management_menu()

    def find_player_id_by_first_name(self):
        db = self.db_players
        find = Query()
        find_first_name = input("\n### Enter the player's first name ###\n")
        players = db.search(find['first name'] == find_first_name)
        if players == []:
            self.view.display_message("\n###There is no such player's first name.###\n")
        else:
            for player in players:
                self.view.display_message(f"\n### Players List number {player['id']} ###")
                for field, value in player.items():
                    player_msg = (f"{field} : {value}, ")
                    self.view.display_message(player_msg)
        self.display_player_management_menu()


    def find_player_id_by_last_name(self):
        db = self.db_players
        find = Query()
        find_first_name = input("\n### Enter the player's last name ###\n")
        players = db.search(find['last name'] == find_first_name)
        if players == []:
            self.view.display_message("\n###There is no such player's first name.###\n")
        else:
            for player in players:
                self.view.display_message(f"\n### Players List number {player['id']} ###")
                for field, value in player.items():
                    player_msg = (f"{field} : {value}, ")
                    self.view.display_message(player_msg)
        self.display_player_management_menu()


    def display_players(self):
        for player_id, player in self.players.items():
            self.view.display_message(f"\n### Players List number {player_id} ###")
            self.view.display_dicts(player.as_dict())
        self.display_player_management_menu()

    def display_tournament_management_menu(self):
        choices = {
            "0": "Create a new tournament",
            "1": "manage a current tournament",
            "2": "Show the finished tournaments",
            "3": "Back",
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            self.create_new_tournament()
        elif user_choice == "1":
            self.display_manage_a_current_tournament_menu()
        elif user_choice == "2":
            self.display_finished_tournament()
        elif user_choice == "3":
            self.display_main_menu()

    def create_new_tournament(self):
        input_fields = Tournament.INPUT_FIELDS
        user_inputs = self.view.get_user_inputs(input_fields)
        user_inputs['player'] = self.add_palyers_to_tournament()
        tournament = Tournament.from_values(user_inputs)
        if Tournament.is_finished(tournament.end_date):
            db = self.db_passed_tournament
            # table_tournament = db.table(user_inputs['name'])
            db.insert(Tournament.as_dict(tournament))
        else :
            # tournament['id'] = self.generate_current_tournament_id()
            db = self.db_current_tournament
            # table_tournament = db.table(user_inputs['name'])
            db.insert(Tournament.as_dict(tournament))
        self.view.display_message(f'The tournament is created !')
        self.display_tournament_management_menu()

    def display_manage_a_current_tournament_menu(self):
        choices = {
            "0": "manage the current tournament by id",
            "1": "show the current tournament",
            "2": "back",
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            self.display_manage_the_current_tournament_by_id_menu()
        elif user_choice == "1":
            self.display_the_current_tournament()
        elif user_choice == "2":
            self.display_tournament_management_menu()

    def display_manage_the_current_tournament_by_id_menu(self):
        tournament_id = input('Please enter the id of the tournament\n')
        self.display_update_tournament_by_id(tournament_id)

    def display_update_tournament_by_id(self, tournament_id):  # ??<<<<<<<<<

        choices = {
            "0": "Generate next round game",
            "1": "Enter the winner information of the last match",
            "2": "update information of the tournament",
            "3": "back"
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            tournament = self.find_tournament_by_id(tournament_id)
            player_list = self.get_player_id_list_from_tournament(tournament)
            list_of_id = Tournament.generate_random_opponent_first_match(player_list)


            list_total = list()
            for listid in list_of_id :
                list_total.append([listid.player_a,listid.player_b])
            kk = {1: 0, 2: 0, 3: 0, 4: 0}
            next_round_list_with_score = Tournament.update_winner_state_match(list_of_id, self.players, kk)
            # print(next_round_list_with_score)
            next_round_list_sorted = Tournament.sort_list_of_players_by_scores(next_round_list_with_score)
            # print(next_round_list_sorted)
            list_of_id = list(next_round_list_sorted.keys())
            # print(list_of_id)
            list_next_round,list_total = Tournament.generate_next_round_match(list_of_id,list_total)
            i =0
            while i<=len(list_of_id):
                next_round_list_with_score = Tournament.update_winner_state_match(list_next_round, self.players,next_round_list_with_score)
                print(next_round_list_with_score)
                next_round_list_sorted = Tournament.sort_list_of_players_by_scores(next_round_list_with_score)
                list_of_id = list(next_round_list_sorted.keys())
                list_next_round, list_total = Tournament.generate_next_round_match(list_of_id, list_total)
                if not list_next_round:
                    break
                else:
                    i += 1
                print(next_round_list_sorted)
            # self.Tournament.generate_random_opponent_first_match()
            # self.display_update_tournament_by_id(tournaments)
        elif user_choice == "1":
            self.find_player_id_by_first_name()
        elif user_choice == "2":
            self.update_information_of_a_tournament(tournament_id)
        elif user_choice == "3":
            self.display_tournament_management_menu()

    def get_player_id_list_from_tournament(self,tournament:Tournament)->list[str]:
        list_player_id = []
        list_player_in_tournament = tournament['List of players participate']
        for sublist in list_player_in_tournament:
            for player in sublist:
                list_player_id.append(player['id'])
        return list_player_id

    def update_information_of_a_tournament(self, find_id:str):
        db = self.db_current_tournament
        tournament = self.find_tournament_by_id(find_id)
        if tournament is not None:
            change_value = self.display_update_tournament_information_menu()
            if change_value == 'List of players participate':
                players = tournament['List of players participate']
                print(f'The player in the tournaments are : {players}')
                players = self.add_palyers_to_tournament()
                db.update({change_value: players}, doc_ids=[int(find_id)])
            elif change_value in ('First match date DD/MM/YYYY','Last match date DD/MM/YYYY'):
                new_value = input(f'please enter the new {change_value}\n')
                new_value_date = datetime.strptime(new_value, "%d/%m/%Y")
                db.update({change_value: new_value_date}, doc_ids=[int(find_id)])
            else :
                new_value = input(f'please enter the new {change_value}\n')
                db.update({change_value: new_value}, doc_ids=[int(find_id)])
            print("Tournament updated successfully!")
        self.display_update_tournament_by_id(find_id)

    def display_the_current_tournament(self):
        tournaments = self.current_tournament
        if len(tournaments) != 0 :
            for tournament_number, tournament in tournaments.items():
                self.view.display_message(f'\n### the list of tournament id {tournament_number} ####')
                self.view.display_dicts(tournament.as_dict())
        else :
            self.view.display_message(f'There is no current tournament')
        self.display_tournament_management_menu()


    def display_finished_tournament(self):
        tournaments = self.passed_tournament
        print(len(tournaments))
        if len(tournaments) != 0 :
            for tournament_number,tournament in tournaments.items():
                self.view.display_message(f'\n### the list of tournament id {tournament_number} ####')
                self.view.display_dicts(tournament.as_dict())
        else :
            self.view.display_message(f'There is no passed tournament')
        self.display_tournament_management_menu()

    def load_tournament_by_id(self, tournament_id:str) :
        tournament_list = []
        tournament_list.append(self.find_tournament_by_id("tournament id", int(tournament_id)))
        if not tournament_list:
            self.view.display_message("There is no such tournament")
            self.display_manage_a_current_tournament_menu()
        else:
            self.display_update_tournament_by_id(tournament_list)

    def generate_user_id(self) -> int:
        # Generate a new user_id that is not already in the database
        # WARNING: to make sure we don't override other players, we need to load the
        # players database before adding a new player
        user_id = len(self.players) + 1
        for player in self.players.values():
            new_id = player.id
            if user_id == new_id:
                user_id = user_id + 1
            return user_id
        return user_id

    # def generate_tournament_id(self) -> int:
    #     tournaments_names = db.tables() # reload json file everytime after a newplayer write to json file
    #     tournament_id = len(tournaments_names) + 1
    #     for tournament_name in tournaments_names:
    #         tournament_document = db.table(tournament_name).all()
    #         new_id = tournament_document['tournament id']
    #         if tournament_id == new_id:
    #             tournament_id = tournament_id + 1
    #         return tournament_id
    #     return tournament_id

    def find_tournament_by_id(self, search_key: str) -> Optional[Tournament]:
        tournament = self.current_tournament
        tournament_found = None
        for tournament_id,tournament in tournament.items():
            if int(search_key) == tournament_id:
                tournament_found = tournament.as_dict()
                self.view.display_message('The tournament is found !')
                break
        if tournament_found is None:
            self.view.display_message("The tournament is not found")
        # print(tournament_found)
        return tournament_found

    def add_palyers_to_tournament(self) ->list[list[Document]]:
        list_player = []
        find = Query()
        choice = 'Y'
        while choice == 'Y' or choice == 'yes' or choice == 'y':
            player_id = input('Please enter the player\'s id to add player\n')
            player = self.db_players.search(find['id'] == int(player_id))
            if player == []:
                self.view.display_message("\n###There is no such player id.###\n")
            else:
                list_player.append(player)
            choice = input('Do you want to add another player Y or N\n')
        return list_player

    def create_a_new_dict(self, listdata: list, new_data: dict):
        # a function that will update a list of players after input manipulations by users
        if listdata is None:
            listdata = []
        listdata.append(update_dicts(new_data))
        return listdata

    # def name_tournament_file(self):
    #     filename = 'tournament'
    #     if not os.path.exists('resources/data'):
    #         os.mkdir('resources/data')
    #     filename = Path('data/' + filename)
    #     return filename

    def reserialization_directory_resources(self, filename):
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(), 'date')
        if not os.path.exists('resources'):
            os.mkdir('resources')
        filename = Path("resources/" + str(filename) + '.json')
        db = TinyDB(filename, storage=serialization)
        return db


# def create_a_new_dict(listdata: list, new_data: dict):
#     # a function that will update a list of players after input manipulations by users
#     if listdata is None:
#         listdata = []
#     listdata.append(update_dicts(new_data))
#     return listdata


# def update_one_dict(dictid: str, listdata: list, key: str):
#     is_in = False
#     for i, data in enumerate(listdata):
#         if player[key] == dictid:
#             listdata[i] = update_dicts(player)
#             is_in = True
#     if is_in == False:
#         print(f"There is no such {dictid}")
#     return listdata


# def display_input_winner(players_opponent):
#     winner = input(f'Please enter the winner of the game {players_opponent[0]} vs '
#                    f'{players_opponent[1]}. '
#                    f'The winner is 1 or 2 or 0 for Draw\n')
#     return winner
#
#
#     def update_winner_state_match(self,list_opponent_in_match:list[str], rounds:str) :
#         """
#         :param list_opponent_in_match: a list contains [every opponents information] in a round
#         :param rounds: round number
#         :return: a list contain two list,list one[opponents information],two [winner],list_opponent_in_match is a dict
#                  contains round number and list player in match with winner
#         """
#         for list_paired in total_list_paired:
#             player1 = self.players.get(int(list_paired[0]))
#             player2 = self.players.get
#             print(f'The winner is 1:{self.players.get(int(find_id))}')
#         # list_player_in_match_with_winner = []
#         # for players_opponent in list_opponent_in_match[rounds]:
#         #     winner = display_input_winner(players_opponent)
#         #     players_opponent.append(winner)
#         #     list_temporary = [players_opponent[i:i + 2] for i in range(0, len(players_opponent), 2)]
#         #     list_player_in_match_with_winner.append(list_temporary)
#         # list_opponent_in_match[rounds] = list_player_in_match_with_winner
#         # return list_player_in_match_with_winner, list_opponent_in_match


# def update_scores_after_match(list_player_in_match_with_winner, list_player_with_score):
#     """
#     update a list player with scores of every player by using another element [0],[1],[2] in list player in match with
#     winner
#     :param list_player_in_match_with_winner: list opponent with another element winner information
#     :param list_player_with_score: list of total players with theirs scores
#     :return: list of total players with theirs scores
#     """
#     i = 0
#     while i < len(list_player_in_match_with_winner):
#         if list_player_in_match_with_winner[i][1] == list("0"):
#             for player_with_score in list_player_with_score:
#                 if player_with_score["player :"] == list_player_in_match_with_winner[i][0][0]:
#                     score = player_with_score["score :"]
#                     score += 0.5
#                     player_with_score.update({"player :": list_player_in_match_with_winner[i][0][0], "score :": score})
#                 elif player_with_score["player :"] == list_player_in_match_with_winner[i][0][1]:
#                     score = player_with_score["score :"]
#                     score += 0.5
#                     player_with_score.update({"player :": list_player_in_match_with_winner[i][0][1], "score :": score})
#         elif list_player_in_match_with_winner[i][1] == list("1"):
#             for player_with_score in list_player_with_score:
#                 if player_with_score["player :"] == list_player_in_match_with_winner[i][0][0]:
#                     score = player_with_score["score :"]
#                     score += 1
#                     player_with_score.update({"score :": score})
#         else:
#             for player_with_score in list_player_with_score:
#                 if player_with_score["player :"] == list_player_in_match_with_winner[i][0][1]:
#                     score = player_with_score["score :"]
#                     score += 1
#                     player_with_score.update({"score :": score})
#
#         i += 1
#     return list_player_with_score  # return a list with [{player:A,score:int},{},{}]





# def sort_list_of_players_by_scores(list_player_with_score):
#     list_player_sorted_by_scores = sorted(list_player_with_score, key=lambda player_with_score:
#     player_with_score.__getitem__(), reverse=True)
#     return list_player_sorted_by_scores



