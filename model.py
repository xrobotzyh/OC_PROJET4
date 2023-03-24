from datetime import datetime
from typing import List


class Player:
    def __init__(self, player_id: int, first_name: str, last_name: str, birthday: datetime, club_id: str = "AB12345"):
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.club_id = club_id

    def as_dict(self):
        player = {
            "Player's id": self.player_id,
            "Player's first name": self.first_name,
            "Player's last name": self.last_name,
            "Player's birthday DD/MM/YYYY": self.birthday,
            "Player's club id": self.club_id
        }
        return player


class Match:
    def __init__(self, player_a: Player, player_b: Player):
        self.player_a = player_a
        self.player_b = player_b
        self.result = None

    def dict_math(self):
        match = {
            "Player A": self.player_a,
            "Player B": self.player_b
        }
        return match


class Tournament:
    def __init__(self, name: str, location: str, start_date: datetime, end_date: datetime, players: List[Player],
                 description: str, number_round: int = 1, total_number_round: int = 4):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_round = number_round
        self.players = players
        self.description = description
        self.total_number_round = total_number_round

    def dict_tournament(self):
        tournament = {
            "Name": self.name,
            "Location": self.location,
            "First match date DD/MM/YYYY": self.date_action,
            "Last match date DD/MM/YYYY": self.date_finish,
            "Total number of round": self.total_number_round,
            "Round": self.number_round,
            "List of players participate": self.players,
            "Descrition of the tournament": self.description
        }
        return tournament

    def is_finished(self):
        now = datetime.now()
        return self.end_date <= now
