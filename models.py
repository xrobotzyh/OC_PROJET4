from typing import List


class Player:
    '''
        a class that contains all the players informations and can calculate the scores after each round
        of the games
    '''

    def __init__(self, id: int, first_name, last_name, birthday, club_id="AB12345"):
        self.id = id or 1
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.club_id = club_id

    def __str__(self):
        informations_player = {
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Birthday": self.birthday,
            "Club": self.club_id
        }
        return f"{informations_player}"


class Match:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.result = None


class TournamentPlayer:
    def __init__(self, player: Player):
        self.player = player
        self.score = 0


class Tournament:
    def __init__(self, players: List[Player], rounds: int, name: str, location: str):
        # Données d'initialisation, constantes
        self.rounds = rounds
        self.name = name
        self.location = location

        # Données qui vont évoluer au cours du temps
        self.players = [TournamentPlayer(player=player) for player in players]
        self.matchs = []  # todo générer les matchs

        # Initialisation des données complexes
        self.init_tournament()

    def init_tournament(self):
        self.matchs = self.generate_matchs()

    def store_match_result(self, match_index, result: MatchResult):
        self.matchs[match_index] = ...
        # TODO