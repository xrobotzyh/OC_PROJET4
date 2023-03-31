from model import Player


class View():

    def __init__(self,header, footer):
        self.header = header
        self.header_main = "*What do you want to do ?\n"
        self.header_add_tournament = "*Please complete the information below"
        self.footer = "please type the number for selecting \n"

    def display_menu(self):

        # a block to show add a new tournament,after the input return to the main menu

        print(self.header_main)
        self.menu = {
            0: "Manage Players",
            1: "Manage tournament",
            2: "Show Reports",
            3: "Load/Sava data",
            4: "Exit"
        }
        self.display_dicts(self.menu)
        choice = input(self.footer)
        return choice

    def display_manage_players_menu(self):
        self.menu = {
            0: "Add a new player",
            1: "Show all the players",
            2: "Updating one player",
            3: "Back"
        }
        self.display_dicts(self.menu)
        choice = input(self.footer)
        return choice

    def display_tournament_manage_menu(self):
        self.menu = {
            0: "Add a new tournament",
            1: "update a tournament",
            2: "Manage the current tournament",
            3: "Show past tournaments",
            4: "Back"
        }
        self.display_dicts(self.menu)
        choice = input(self.footer)
        return choice

    def display_exit(self):
        print("See you next time !")
        exit()
    def display_show_rapports_memu(self):
        pass

    def display_data_menu(self):
        pass

    def display_add_new_player(self):
        answer = "Y"
        new_player = []
        while answer == "Y":
            new_player.append(input(self.update_dicts(Player(None, None, None, None, None).get_player())))
            answer = input("Do you want to add a player? Y or N\n")
        return new_player   #list

    def display_add_new_tournament_menu(self):

        # a block to show add a new tournament,after the input return to the main menu

        tournament = Tournament().get_tournament()  # initialization data
        tournament.pop("List of players participate")  # delete the element "player" handle it separately
        print(self.header_main)
        print(self.header_add_tournament)
        tournament = update_dicts(tournament)
        player = []
        reponse = input("Do you want to add player? Y/N \n")
        while reponse in ["y", "Y"]:
            player = create_a_new_player(player)
            reponse = input("Do you want to add player? Y/N \n")
        tournament.update({"List of players participate": player})
        print(display_dicts(tournament))
        return tournament

    def display_current_tournament(self, tournaments):
        print(self.header_main)
        tournament = Tournament()
        for index, tournament in enumerate(tournaments):
            print(f'{index + 1} : {tournament["Name"]}')
        choice = input("\n*Select the tournament you want to manage by typing its number \n")
        return choice

    def display_manage_tournament(self):
        print(self.header_main)
        dict_manage_tournament = {
            0: "Add a new player to the tournament",
            1: "Generate next match",
            2: "Add the result of last round",
            3: "Show the history results"
        }
        display_dicts(dict_manage_tournament)
        choice = input(self.footer)
        return choice

    def display_previous_tournament(self, tournaments):
        print(self.header_main)
        tournament = Tournament()
        for index, tournament in enumerate(tournaments):
            print(f'{index + 1} : {tournament["Name"]}')
        choice = input("\n*Select the tournament you want to manage by typing its number \n")
        return choice

    def display_no_tournament_at_this_moment(self):
        if not os.path.exists('resources') or len(new_tournaments) == 0:
            print('**//!!!There is no tournament for the moment!!!//**\n\n\n')


    def display_dicts(self,dicts):
        # a function that will show the dictionary line by line

        for key, value in dicts.items():
            print(f'{key}:{value}')

    def display_lists(self,lists):
        for i in range(len(lists)):
            print(i)


    def update_dicts(self,dict):
        # a function that will update the data after input manipulations by users
        new_dict = {}
        for key, value in dict.items():
            value = input(f'Please enter the {key}\n')
            key = key
            new_dict.update({key: value})
        return new_dict



    def update_one_player(self,playerid:str,listplayers:list):
        for player in listplayers :
            if player["Player's id"] == playerid:
                update_dicts(player)
            else :
                print(f"There is no such player with id {playerid}")

