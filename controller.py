import os
from pathlib import Path
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

        self.tournaments = {}
        self.current_tournament = None
        db = self.reserialization_directory_resources('players')
        self.players = db.all()
        db.close()



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
            self.view.display_show_rapports_memu()
        elif user_choice == "4":
            self.view.display_message("\nSee you next time !\n")
            exit(0)



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

    def create_new_player(self):
        input_fields = Player.INPUT_FIELDS
        user_inputs = self.view.get_user_inputs(input_fields)
        user_inputs['id'] = self.generate_user_id()
        player = Player.from_values(user_inputs)
        player_dicts_forma = Player.as_dict(player)
        print(player_dicts_forma)
        db = self.reserialization_directory_resources('players')
        db.insert(player_dicts_forma)
        db.close()
        self.display_player_management_menu()

    def update_player_by_id(self):
        db = self.reserialization_directory_resources('players')
        db.all()
        find = Query()
        find_id = input("\n### Enter the id ###\n")
        player = db.search(find['id'] == int(find_id))
        if player == []:
            self.view.display_message("\n###There is no such player id.###\n")
        else:
            input_fields = Player.INPUT_FIELDS
            user_inputs = self.view.get_user_inputs(input_fields)
            user_inputs['id'] = int(find_id)
            player = Player.from_values(user_inputs)
            player_dicts_forma = Player.as_dict(player)
            db.update(player_dicts_forma, find['id'] == int(find_id))
        self.display_player_management_menu()
        db.close()

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
        db = self.reserialization_directory_resources('players')
        db.all()
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
        db.close()

    def find_player_id_by_last_name(self):
        db = self.reserialization_directory_resources('players')
        db.all()
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
        db.close()

    def display_players(self):
        db = self.reserialization_directory_resources('players')
        players = db.all()
        db.close()
        player_msg = ''
        for player in players:
            self.view.display_message(f"\n### Players List number {player['id']} ###")
            #     print(player)
            for field, value in player.items():
                player_msg = (f"{field} : {value}, ")
                self.view.display_message(player_msg)
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
        user_inputs['id'] = self.generate_tournament_id()
        user_inputs['player'] = self.add_palyers_to_tournament()
        tournament = Tournament.from_values(user_inputs)
        tournament_dicts_forma = Tournament.as_dict(tournament)
        print(tournament_dicts_forma)
        filename = self.name_tournament_file()
        db = self.reserialization_directory_resources(filename)
        table_tournament = db.table(user_inputs['name'])
        table_tournament.insert(tournament_dicts_forma)
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
        tournament = input('Please enter the id of the tournament\n')
        self.load_tournament_by_id(tournament)

    def display_update_tournament_by_id(self, tournaments):  # ??<<<<<<<<<

        choices = {
            "0": "Generate next round game",
            "1": "Enter the winner information of the last match",
            "2": "update information of the tournament",
            "3": "back"
        }
        user_choice = self.view.display_menu(choices)  # show the main menu
        if user_choice == "0":
            db = self.reserialization_directory_resources('data/tournament')
            list_player = tournaments[0][0][0]['List of players participate']
            print(list_player[0])
            # for tournament in list(tournaments['List of players participate'][0]) :
            #     listplayer.append(tournament)
            # print(tournaments[0]['List of players participate'])
            # match = generate_random_opponent_first_match(listplayer)
            # print(match)
            self.display_update_tournament_by_id(tournaments)
        elif user_choice == "1":
            self.find_player_id_by_first_name()
        elif user_choice == "2":
            self.update_information_of_a_tournament(tournaments)
        elif user_choice == "3":
            self.display_tournament_management_menu()


    def update_information_of_a_tournament(self,tournaments):
        db = self.reserialization_directory_resources('data/tournament')
        table = db.table(tournaments[0][0][0]['Name'])         #--------> ??????
        input_fields = Tournament.INPUT_FIELDS
        user_inputs = self.view.get_user_inputs(input_fields)
        user_inputs['id'] = tournaments[0][0][0]['tournament id']
        user_inputs['player'] = self.add_palyers_to_tournament()
        tourna = Tournament.from_values(user_inputs)
        tournament_dicts_forma = Tournament.as_dict(tourna)
        print(tournament_dicts_forma)
        table.update(tournament_dicts_forma)
        self.display_update_tournament_by_id(tournaments)

    def display_the_current_tournament(self):
        db = self.reserialization_directory_resources('data/tournament')
        finish_date = Query()
        now = datetime.now()
        tables_name = db.tables()
        for table_name in tables_name:
            table = db.table(table_name)
            tournaments = table.search(finish_date["Last match date DD/MM/YYYY"] >= now)
            for tournament in tournaments:
                self.view.display_message(f"\n### Tournaments List {tournament['tournament id']} ###")
                for field, value in tournament.items():
                    tournament_msg = (f"{field} : {value}, ")
                    self.view.display_message(tournament_msg)
        db.close()
        self.display_tournament_management_menu()

    def display_finished_tournament(self):
        db = self.reserialization_directory_resources('data/tournament')
        finish_date = Query()
        now = datetime.now()
        tables_name = db.tables()
        for table_name in tables_name:
            table = db.table(table_name)
            tournaments = table.search(finish_date["Last match date DD/MM/YYYY"] < now)
            for tournament in tournaments:
                self.view.display_message(f"\n### Tournaments List {tournament['tournament id']} ###")
                for field, value in tournament.items():
                    tournament_msg = (f"{field} : {value}, ")
                    self.view.display_message(tournament_msg)
        db.close()
        self.display_tournament_management_menu()

    def load_tournament_by_id(self, tournament_id):
        tournament_list = []
        tournament_list.append(self.find_value_in_all_tables_tournament("tournament id",int(tournament_id)))
        if not tournament_list:
            self.view.display_message("There is no such tournament")
            self.display_manage_a_current_tournament_menu()
        else:
            self.display_update_tournament_by_id(tournament_list)





    def generate_user_id(self) -> int:
        # Generate a new user_id that is not already in the database
        # WARNING: to make sure we don't override other players, we need to load the
        # players database before adding a new player
        db = self.reserialization_directory_resources('players')
        self.players = db.all()  # reload json file everytime after a newplayer write to json file
        db.close()
        user_id = len(self.players) + 1
        for player in self.players:
            value = list(player.values())
            new_id = value[0]
            if user_id == new_id:
                user_id = user_id + 1
            return user_id
        return user_id

    def generate_tournament_id(self) -> int:
        db = self.reserialization_directory_resources('data/tournament')
        tournaments = db.tables()  # reload json file everytime after a newplayer write to json file
        tournament_id = len(tournaments) + 1
        for tournament in tournaments:
            table = db.table(tournament)
            tournament = table.all()
            new_id = tournament[0]['tournament id']
            if tournament_id == new_id:
                tournament_id = tournament_id + 1
            return tournament_id
        return tournament_id

    def find_value_in_all_tables_tournament(self,search_key:str,value:str) -> list:
        db = self.reserialization_directory_resources('data/tournament')
        q_obj = Query()
        table_names = db.tables()
        tournament_list = []
        for table_name in table_names:
            table = db.table(table_name)
            tournaments = table.search(q_obj[search_key]==value)
            if not tournaments:
                pass
            else:
                tournament_list.append(tournaments)
        db.close()
        return tournament_list


    def add_palyers_to_tournament(self):
        list_player = []
        db = self.reserialization_directory_resources('players')
        db.all()
        find = Query()
        choice = 'Y'
        while choice == 'Y' or choice == 'yes' or choice == 'y':
            player_id = input('Please enter the player\'s id to add player\n')
            player = db.search(find['id'] == int(player_id))
            if player == []:
                self.view.display_message("\n###There is no such player id.###\n")
            else:
                list_player.append(player)
            choice = input('Do you want to add another player Y or N\n')
        db.close()
        return list_player



    def create_a_new_dict(self, listdata: list, new_data: dict):
        # a function that will update a list of players after input manipulations by users
        if listdata is None:
            listdata = []
        listdata.append(update_dicts(new_data))
        return listdata

    def name_tournament_file(self):
        filename = 'tournament'
        if not os.path.exists('resources/data'):
            os.mkdir('resources/data')
        filename = Path('data/' + filename)
        return filename

    def reserialization_directory_resources(self, filename):
        serialization = SerializationMiddleware(JSONStorage)
        serialization.register_serializer(DateTimeSerializer(), 'date')
        if not os.path.exists('resources'):
            os.mkdir('resources')
        filename = Path("resources/" + str(filename) + '.json')
        db = TinyDB(filename, storage=serialization)
        return db


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


def display_input_winner(players_opponent):
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
        winner = display_input_winner(players_opponent)
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


def sort_list_of_players_by_scores(list_player_with_score):
    list_player_sorted_by_scores = sorted(list_player_with_score, key=lambda player_with_score:
    player_with_score.__getitem__("score :"), reverse=True)
    return list_player_sorted_by_scores


def generate_next_round_match(list_player_with_score):
    list_player_next_round = []
    for player_with_score in list_player_with_score:
        list_player_next_round.append(player_with_score["player :"])  # a list without scores informations but sorted
