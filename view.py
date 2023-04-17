from typing import Dict, Any


class View:

    def __init__(self, header, footer):
        self.header = header
        self.header_main = "\n*What do you want to do ?"
        self.header_add_tournament = "*Please complete the information below"
        self.footer = "\nPlease type the number for selecting \n"

    def display_menu(self, choices: Dict[str, str]):

        # a block to show add a new tournament,after the input return to the main menu
        print(self.header_main)
        choice = None
        self.display_dicts(choices)
        while choice not in choices:
            choice = input(self.footer)
        return choice

    def get_user_inputs(self, input_fields: Dict[str, Any]) -> Dict[str, str]:
        # Note for improvements: user input validation
        user_inputs = {}
        for key, value in input_fields.items():
            value = input(f'Input for {value}\n')
            user_inputs[key] = value
        return user_inputs

    def get_user_input(self, prompt: str) -> str:
        # Note for improvements: user input validation
        return input(f'{prompt}\n')

    def display_message(self, message):
        print(message)

    # def _display_lists(self, lists):
    #     for i in range(len(lists)):
    #         print(i)
    def display_dicts(self, dicts):
        # a function that will show the dictionary line by line

        for key, value in dicts.items():
            print(f'{key}: {value}')

    # def display_add_new_tournament_menu(self):
    #
    #     # a block to show add a new tournament,after the input return to the main menu
    #
    #     tournament = Tournament().get_tournament()  # initialization data
    #     tournament.pop("List of players participate")  # delete the element "player" handle it separately
    #     print(self.header_main)
    #     print(self.header_add_tournament)
    #     tournament = update_dicts(tournament)
    #     player = []
    #     reponse = input("Do you want to add player? Y/N \n")
    #     while reponse in ["y", "Y"]:
    #         player = create_a_new_player(player)
    #         reponse = input("Do you want to add player? Y/N \n")
    #     tournament.update({"List of players participate": player})
    #     print(display_dicts(tournament))
    #     return tournament
    #
    # def display_current_tournament(self, tournaments):
    #     print(self.header_main)
    #     tournament = Tournament()
    #     for index, tournament in enumerate(tournaments):
    #         print(f'{index + 1} : {tournament["Name"]}')
    #     choice = input("\n*Select the tournament you want to manage by typing its number \n")
    #     return choice
    #
    # def display_manage_tournament(self):
    #     print(self.header_main)
    #     dict_manage_tournament = {
    #         0: "Add a new player to the tournament",
    #         1: "Generate next match",
    #         2: "Add the result of last round",
    #         3: "Show the history results"
    #     }
    #     display_dicts(dict_manage_tournament)
    #     choice = input(self.footer)
    #     return choice

    # def display_previous_tournament(self, tournaments):
    #     print(self.header_main)
    #     tournament = Tournament()
    #     for index, tournament in enumerate(tournaments):
    #         print(f'{index + 1} : {tournament["Name"]}')
    #     choice = input("\n*Select the tournament you want to manage by typing its number \n")
    #     return choice

    # def display_no_tournament_at_this_moment(self):
    #     if not os.path.exists('resources') or len(new_tournaments) == 0:
    #         print('**//!!!There is no tournament for the moment!!!//**\n\n\n')
    #
