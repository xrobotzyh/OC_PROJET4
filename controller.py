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
import re


class Controller:

    def __init__(self):

        self.view = View(
            header="----------------------------------------\n| Welcome to Chess Tournament Software "
                   "|\n----------------------------------------",
            footer="\n*Select the command by typing the number\n",
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
        user_choice = self.view.display_main_menu(choices)  # show the main menu
        if user_choice == "0":
            self.display_player_management_menu()
        elif user_choice == "1":
            self.display_tournament_management_menu()
        elif user_choice == "2":
            self.display_reports_menu()
        elif user_choice == "3":
            self.load_save()
            self.display_main_menu()
        elif user_choice == "4":
            choice = self.view.get_user_input("Do you want to save your change? Y or N")
            if choice in ["Y", "y"]:
                self.load_save()
            else:
                pass
            self.view.display_message("\nSee you next time !\n")
            exit(0)

    def load_save(self):
        for id_tournament, tournament in self.tournaments.items():
            self.db_tournament.update(tournament.to_json(), doc_ids=[id_tournament])
        self.__init__()

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
        self.__init__()
        # reload the menu
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
        db.close()
        self.__init__()
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
        if not players:
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
        # find last name in database
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
            db.insert(Tournament.to_json(tournament))
        else:
            db = self.db_tournament
            db.insert(Tournament.to_json(tournament))
        self.view.display_message(f'The tournament is created !')
        db.close()
        self.__init__()
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
        # function to get input value of winner information for matches in round and calculate the scores
        # of players in match
        round = self.current_tournament.rounds[-1]
        if not round.end_time:
            for match in round.matches:
                # get input winner information
                result = self.view.get_user_input(f"Enter match result player id {match.player_a[0]} VS player id "
                                                  f"{match.player_b[0]},The winner is 1 for "
                                                  f"{match.player_a[0].first_name} {match.player_a[0].last_name}, 2 "
                                                  f"for {match.player_b[0].first_name} {match.player_b[0].last_name}, "
                                                  f"or 3 for tie  ")
                match.set_result(result)
                match.result = result
        else:
            self.view.display_message('You have entered the winner information for the last round')
        for match in round.matches:
            player_a_id = str(match.player_a[0].id)
            player_b_id = str(match.player_b[0].id)

            # update scores according to winner information
            score_a = self.current_tournament.players_scores.get(player_a_id) + match.player_a[1]
            score_b = self.current_tournament.players_scores.get(player_a_id) + match.player_b[1]
            self.current_tournament.players_scores.update({player_a_id: score_a})
            self.current_tournament.players_scores.update({player_b_id: score_b})
            print(match.result)
        print(self.current_tournament.players_scores)
        self.current_tournament.current_round_number += 1
        self.current_tournament.rounds[-1].close()
        # self.load_save()

    def display_update_tournament_by_id(self):

        choices = {
            "0": "Generate next round game",
            "1": "Enter the winner information of the last match",
            "2": "update information of the tournament",
            "3": "back"
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            # if it is the first round
            if not self.current_tournament.rounds:
                self.current_tournament.start()
            else:
                # if the last round result has not been entered
                if not self.current_tournament.rounds[-1].matches[
                    0].result:  # if not self.current_tournament.rounds[-1].matches[-1].result:
                    self.view.display_message(f'Please enter the winner information for last round!')
                else:
                    # if it is not the first round and the last round winner information has been entered
                    # go to next round
                    self.current_tournament.go_to_next_round()
            self.display_update_tournament_by_id()
        elif user_choice == "1":
            # if the current round is start and result has not been entered, get the information and sort
            # the player list by their scores
            if not self.current_tournament.rounds:
                self.view.display_message('The match is not start !')
            elif not self.current_tournament.rounds[-1].matches[0].result:
                self.current_tournament_enter_round_results()
                self.current_tournament.sort_list_of_players_by_scores()
            else:
                # if the current round is start and result has been entered,
                self.view.display_message('Your haves entered the winner information')
            self.display_update_tournament_by_id()
        elif user_choice == "2":
            self.update_information_of_a_tournament()
        elif user_choice == "3":
            self.display_tournament_management_menu()

    def update_information_of_a_tournament(self):
        change_value = self.display_update_tournament_information_menu()
        if change_value == "player_ids":
            # check if the match is start,if started, can not update player list
            if not self.current_tournament.rounds:
                players = []
                for player in self.current_tournament.players:
                    players.append(str(player))
                self.view.display_message(f'The player in the tournaments are : {players}')
                new_value_player = self.add_players_to_tournament()
                self.current_tournament.players = new_value_player
            else:
                self.view.display_message('You can not edit the players list,because the match is started!')
                self.display_update_tournament_by_id()
        elif change_value in ('start_date', 'end_date'):
            # check if the match is start,if started, can not update date information
            if not self.current_tournament.rounds:
                new_value_date = self.view.get_user_input(f'please enter the new {change_value}')
                new_value = datetime.strptime(new_value_date, "%d/%m/%Y")
                setattr(self.current_tournament, change_value, new_value)
            else:
                self.view.display_message('You can not edit this information,because the match is started!')
        else:
            new_value = self.view.get_user_input(f'please enter the new {change_value}')
            setattr(self.current_tournament, change_value, new_value)
        self.view.display_message("Tournament updated successfully!")
        # self.load_save()
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
        return list_player

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

    def display_reports_menu(self):
        choices = {
            "0": "print all players in alphabetical order",
            "1": "print list of all tournaments",
            "2": "print the name and dates of a given tournament",
            "3": "print list of players in the tournament in alphabetical order",
            "4": "print list of all rounds and matches of a tournament",
            "5": "back"

        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            report_title, columns, report_data = self.report_of_all_players_in_alphabetical_order()
            self.generate_report(report_title, columns, report_data)
        elif user_choice == "1":
            report_title, columns, report_data = self.report_of_all_tournaments()
            self.generate_report(report_title, columns, report_data)
        elif user_choice == "2":
            report_title, columns, report_data = self.report_of_a_tournament_given()
            self.generate_report(report_title, columns, report_data)
        elif user_choice == "3":
            report_title, columns, report_data = self.report_players_in_tournament()
            self.generate_report(report_title, columns, report_data)
        elif user_choice == "4":
            report_title, columns, report_data = self.report_round_and_match_information_of_a_tournament()
            self.generate_report(report_title, columns, report_data)
        else:
            self.display_main_menu()
        self.display_reports_menu()

    def generate_report(self, report_title: str, columns: list[str], report_data: list[dict]):
        # get three attributes to generate with html template
        filename = re.sub(r"\s+", "_", report_title)
        template = self.view.display_report_template()
        report_html = template.render(report_title=report_title, columns=columns, report_data=report_data)
        filename = Path("resources/data/" + filename + ".html")
        with open(filename, 'w') as f:
            f.write(report_html)
        self.view.display_message('report generate successfully !')

    def report_of_all_players_in_alphabetical_order(self):
        report_title = 'report of all players in alphabetical order'
        columns = ['first name', 'last name', 'birthday', 'club id']
        sorted_player_list = sorted(self.players.values(), key=lambda x: x.first_name)
        report_data = []
        for player in sorted_player_list:
            report_data.append({
                'first name': player.first_name,
                'last name': player.last_name,
                'birthday': player.birthday,
                'club id': player.club_id
            })
        return report_title, columns, report_data

    def report_of_all_tournaments(self):
        report_title = 'list of all tournaments'
        columns = ['name', 'location', 'start date', 'end date']
        report_data = []
        for tournament in self.tournaments.values():
            report_data.append({
                'name': tournament.name,
                'location': tournament.location,
                'start date': tournament.start_date,
                'end date': tournament.end_date
            })
        for tournament in self.passed_tournament.values():
            report_data.append({
                'name': tournament.name,
                'location': tournament.location,
                'start date': tournament.start_date,
                'end date': tournament.end_date
            })
        return report_title, columns, report_data

    def report_of_a_tournament_given(self):
        tournament_id = self.view.get_user_input('Please enter the id of the tournament')
        tournament = self.find_tournament_by_id(tournament_id)
        report_title = 'report of name and date for' + ' ' + str(tournament.name)
        columns = ['name', 'start date', 'end date']
        report_data = [{
            'name': tournament.name,
            'start date': tournament.start_date,
            'end date': tournament.end_date
        }]
        return report_title, columns, report_data

    def report_players_in_tournament(self):
        tournament_id = self.view.get_user_input('Please enter the id of the tournament')
        tournament = self.find_tournament_by_id(tournament_id)
        sorted_list_player = sorted(tournament.players, key=lambda x: x.first_name)
        report_title = 'report of all players in tournament ' + ' ' + str(tournament.name)
        columns = ['id', 'first name', 'last name', 'club id']
        report_data = []
        for player in sorted_list_player:
            report_data.append({
                'id': player.id,
                'first name': player.first_name,
                'last name': player.last_name,
                'club id': player.club_id
            })
        return report_title, columns, report_data

    def report_round_and_match_information_of_a_tournament(self):
        tournament_id = self.view.get_user_input('Please enter the id of the tournament')
        tournament = self.find_tournament_by_id(tournament_id)
        report_title = 'report of round and match information of tournament' + ' ' + str(tournament.name)
        columns = ['round name', 'match', 'winner', 'round start date', 'round end date']
        report_data = []
        for round in tournament.rounds:
            for match in round.matches:
                if match.result == '1':
                    winner = match.player_a[0].first_name + ' ' + match.player_a[0].last_name
                elif match.result == '2':
                    winner = match.player_b[0].first_name + ' ' + match.player_b[0].last_name
                else:
                    winner = 'Tie'
                # match_information = match.player_a[0].first_name + ' ' + match.player_a[0].last_name + ' VS ' + \
                #                     match.player_b[0].first_name + ' ' + match.player_b[0].last_name
                report_data.append({
                    'round name': round.name,
                    'match': match,
                    'winner': winner,
                    'round start date': round.start_time,
                    'round end date': round.end_time
                })
        return report_title, columns, report_data
