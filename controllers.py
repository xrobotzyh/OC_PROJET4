from models import Player
from views import ConsoleView


class AppController:
    def __init__(self):
        self.players = dict()
        self.view = ConsoleView()

    def add_player(self, player: Player):
        self.players[player.id] = player

    def update_player(self, player_id: int, updated_player: Player):
        self.players[player_id] = updated_player

    def display_home_menu(self):
        title = 'Accueil'
        choices = [
            "Gestion des joueurs",
            "Gestion des tournois",
            "Charger / sauvegarder des données",
            "Quitter",
        ]
        choice = self.view.show_choices(title, choices)
        if choice == 1:
            self.display_player_management_menu()
        elif choice == 2 or choice == 3:
            self.display_not_implemented()
        else:
            print('Bye!')
            exit(0)

    def display_player_management_menu(self):
        print("Gestion des joueurs")
        exit(0)

    def display_not_implemented(self):
        print("A faire!")
        exit(1)
