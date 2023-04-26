import os
from pathlib import Path
from typing import Dict, Optional, List
import random

from tinydb.table import Document

from view import View
from model import Player, Tournament, Match
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

        # self.db_passed_tournament: Optional[Tournament] = None
        self.db_players = self.reserialization_directory_resources('players')
        self.db_tournament = self.reserialization_directory_resources('/data/tournament')
        self.db_passed_tournament = self.reserialization_directory_resources('/data/passed_tournament')

        self.players: Dict[int, Player] = self.load_players_from_db()
        self.current_tournament: Tournament = None
        self.tournaments: Dict[int, Tournament] = self.load_tournaments_from_db('/data/tournament')
        # self.current_tournament: Dict[int, Tournament] = self.load_tournaments_from_db('/data/current_tournament')
        self.passed_tournament: Dict[int, Tournament] = self.load_tournaments_from_db('/data/passed_tournament')

    def load_players_from_db(self) -> Dict[int, Player]:
        db = self.db_players.all()
        players_documents: List[Document] = db
        players = {}
        for player_document in players_documents:
            players[player_document.doc_id] = Player.from_json(player_document)
        return players

    def load_tournaments_from_db(self, filename) -> Dict[int, Tournament]:

        if filename == '/data/tournament':
            db = self.db_tournament
        else:
            db = self.db_passed_tournament
        tournaments_document = db.all()
        tournaments = {}
        for tournament_document in tournaments_document:
            tournaments[tournament_document.doc_id] = Tournament.from_json(tournament_document, players_db=self.players)
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
            self.view.display_reports_menu()  # TODO
        elif user_choice == "3":
            self.load_save()
        elif user_choice == "4":
            self.view.display_message("\nSee you next time !\n")
            exit(0)

    def load_save(self):
        for id_tournament, tournament in self.tournaments.items():
            self.db_tournament.update(tournament.to_json(), doc_ids=[id_tournament])
        # for document in self.db_current_tournament:
        #     print(document.doc_id)
        # self.db_passed_tournament.update(self.passed_tournament, doc_ids=self.db_passed_tournament.all_ids())
        #     self.db_current_tournament.update(self.current_tournament, doc_ids=[1,2])
        # self.db_current_tournament.write_back()
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

    def display_update_player_information_menu(self) -> str:
        choices = {
            "0": "Edit the player's first name",
            "1": "Edit the player's last name",
            "2": "Edit the player's birthday",
            "3": "Edit the player's club id",
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        value = ''
        if user_choice == "0":
            value = 'first name'
        elif user_choice == "1":
            value = 'last name'
        elif user_choice == "2":
            value = 'birthday DD/MM/YYYY'
        elif user_choice == "3":
            value = 'club id'
        return value

    def display_update_tournament_information_menu(self) -> str:
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
            value = 'name'
            return value
        elif user_choice == "1":
            value = 'location'
            return value
        elif user_choice == "2":
            value = 'start_date'
            return value
        elif user_choice == "3":
            value = 'end_date'
            return value
        elif user_choice == "4":
            value = 'total_round_number'
            return value
        elif user_choice == "5":
            value = 'player_ids'
            return value
        elif user_choice == "6":
            value = 'description'
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
        db.insert(Player.to_json(player))
        db.close()
        self.db_players = self.reserialization_directory_resources('players')
        self.players = self.load_players_from_db()
        # player.id = player_id

        self.display_player_management_menu()

    def update_player_by_id(self):
        db = self.db_players
        find_id = self.view.get_user_input("\n### Enter the id ###\n")
        # ODO cleanup du controller, il ne doit pas gérer les entrées / sorties, c'est le role de la view
        player = self.players.get(int(find_id))
        if player:
            change_value = self.display_update_player_information_menu()
            new_value = self.view.get_user_input(f'please enter the new {change_value}\n')
            db.update({change_value: new_value}, doc_ids=[player.id])
            self.view.display_message("Player updated successfully!")
        else:
            self.view.display_message(f"No such a player")
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
        find_first_name = self.view.get_user_input("\n### Enter the player's first name ###\n")
        players = db.search(find['first name'] == find_first_name)
        if players == []:
            self.view.display_message("\n###There is no such player's first name.###\n")
        else:
            for player in players:
                self.view.display_message(f"\n### Players List number {player['id']} ###")
                for field, value in player.items():
                    player_msg = f"{field} : {value},"
                    self.view.display_message(player_msg)
        self.display_player_management_menu()

    def find_player_id_by_last_name(self):
        db = self.db_players
        find = Query()
        find_first_name = self.view.get_user_input("\n### Enter the player's last name ###\n")
        players = db.search(find['last name'] == find_first_name)
        if not players:
            self.view.display_message("\n###There is no such player's first name.###\n")
        else:
            for player in players:
                self.view.display_message(f"\n### Players List number {player['id']} ###")
                for field, value in player.items():
                    player_msg = f"{field} : {value}, "
                    self.view.display_message(player_msg)
        self.display_player_management_menu()

    def display_players(self):
        for player_id, player in self.players.items():
            self.view.display_message(str(player))
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
        user_inputs['players'] = self.add_players_to_tournament()
        tournament = Tournament.from_values(user_inputs)
        if tournament.is_finished():
            db = self.db_passed_tournament
            # table_tournament = db.table(user_inputs['name'])
            db.insert(Tournament.to_json(tournament))
        else:
            # tournament['id'] = self.generate_current_tournament_id()
            db = self.db_tournament
            # table_tournament = db.table(user_inputs['name'])
            db.insert(Tournament.to_json(tournament))
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
            self.display_the_tournament()
        elif user_choice == "2":
            self.display_tournament_management_menu()

    def display_manage_the_current_tournament_by_id_menu(self):
        tournament_id = self.view.get_user_input('Please enter the id of the tournament')
        self.load_tournament_by_id(tournament_id)
        self.display_update_tournament_by_id()

    def current_tournament_enter_round_results(self):
        round = self.current_tournament.rounds[-1]
        if not round.end_time:
            for match in round.matches:
                result = self.view.get_user_input(f"Enter match result {match},The winner is 1 for "
                                                  f"player A, 2 for player B, or 3 for tie  ")
                match.set_result(result)
                match.result = result
        else:
            self.view.display_message('You have entered the winner information for the last round')
        for match in round.matches:
            player_a_id = str(match.player_a[0].id)
            player_b_id = str(match.player_b[0].id)
            score_a = self.current_tournament.players_scores.get(player_a_id) + match.player_a[1]
            score_b = self.current_tournament.players_scores.get(player_b_id) + match.player_b[1]
            self.current_tournament.players_scores.update({player_a_id: score_a})
            self.current_tournament.players_scores.update({player_b_id: score_b})
            print(match.result)
        print(self.current_tournament.players_scores)
        self.current_tournament.current_round_number += 1
        self.current_tournament.rounds[-1].close()


    def display_update_tournament_by_id(self):

        choices = {
            "0": "Generate next round game",
            "1": "Enter the winner information of the last match",
            "2": "update information of the tournament",
            "3": "back"
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            if not len(self.current_tournament.rounds):
                self.current_tournament.start()
            else:
                if not self.current_tournament.rounds[-1].matches[-1].result:
                    self.view.display_message(f'Please enter the winner information for last round!')
                else:
                    self.current_tournament.go_to_next_round()
            self.display_update_tournament_by_id()
        elif user_choice == "1":
            if not self.current_tournament.rounds[-1].matches[-1].result:
                self.current_tournament_enter_round_results()
                self.current_tournament.sort_list_of_players_by_scores()
            else:
                self.view.display_message('Your haves entered the winner information')
            self.display_update_tournament_by_id()
        elif user_choice == "2":
            self.update_information_of_a_tournament()
        elif user_choice == "3":
            self.display_tournament_management_menu()

    def update_information_of_a_tournament(self):
        change_value = self.display_update_tournament_information_menu()
        if change_value == "player_ids":
            if not self.current_tournament.rounds[-1].matches[0]:
                self.view.display_message(
                    f'The player in the tournaments are : {self.current_tournament.players.__str__()}')
                new_value_player = self.add_players_to_tournament()
                self.current_tournament.players = new_value_player
            else :
                self.view.display_message('You can not edit the players list,because the match is started!')
        elif change_value in ('start_date', 'end_date'):
            if not self.current_tournament.rounds[-1].matches[0]:
                new_value_date = self.view.get_user_input(f'please enter the new {change_value}')
                new_value = datetime.strptime(new_value_date, "%d/%m/%Y")
                setattr(self.current_tournament, change_value, new_value)
            else:
                self.view.display_message('You can not edit this information,because the match is started!')
        else:
            new_value = self.view.get_user_input(f'please enter the new {change_value}')
            setattr(self.current_tournament, change_value, new_value)
        self.view.display_message("Tournament updated successfully!")
        self.display_update_tournament_by_id()

    def display_the_tournament(self):
        tournaments = self.tournaments
        if len(tournaments) != 0:
            for tournament_number, tournament in tournaments.items():
                self.view.display_message(f'\n### the list of tournament id {tournament_number} ####')
                self.view.display_dicts(tournament.as_dict())
        else:
            self.view.display_message(f'There is no finished tournament')
        self.display_tournament_management_menu()

    def display_finished_tournament(self):
        tournaments = self.passed_tournament
        print(len(tournaments))
        if len(tournaments) != 0:
            for tournament_number, tournament in tournaments.items():
                self.view.display_message(f'\n### the list of tournament id {tournament_number} ####')
                self.view.display_dicts(tournament.as_dict())
        else:
            self.view.display_message(f'There is no passed tournament')
        self.display_tournament_management_menu()

    def load_tournament_by_id(self, tournament_id: str):
        tournament_found = self.find_tournament_by_id(tournament_id)
        if not tournament_found:
            self.view.display_message("There is no such tournament")
            self.current_tournament = tournament_found
            self.display_manage_a_current_tournament_menu()
        else:
            self.display_update_tournament_by_id()

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
        tournaments = self.tournaments
        tournament_found = None
        for tournament_id, tournament in tournaments.items():
            if int(search_key) == tournament_id:
                tournament_found = tournament
                self.current_tournament = tournament_found
                self.view.display_message('The tournament is found !')
                break
        if tournament_found is None:
            self.view.display_message("The tournament is not found")
        # print(tournament_found)
        return self.current_tournament

    def add_players_to_tournament(self) -> list[list[Document]]:
        list_player = []
        find = Query()
        choice = 'Y'
        while choice == 'Y' or choice == 'yes' or choice == 'y':
            player_id = self.view.get_user_input('Please enter the player\'s id to add player')
            player = self.db_players.search(find['id'] == int(player_id))[0]
            if not player:
                self.view.display_message("\n###There is no such player id.###\n")
            else:
                list_player.append(Player.from_json(player))
            choice = self.view.get_user_input('Do you want to add another player Y or N')
            # list_player_obj = Player.from_json(list_player)
        return list_player

    # def create_a_new_dict(self, listdata: list, new_data: dict):
    #     # a function that will update a list of players after input manipulations by users
    #     if listdata is None:
    #         listdata = []
    #     listdata.append(update_dicts(new_data))
    #     return listdata

    def reserialization_directory_resources(self, filename):
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(), 'date')
        if not os.path.exists('resources'):
            os.mkdir('resources')
        if not os.path.exists('resources/data'):
            os.mkdir('resources/data')
        filename = Path("resources/" + str(filename) + '.json')
        db = TinyDB(filename, storage=serialization)
        return db
