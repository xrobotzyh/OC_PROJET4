from random import random
from typing import List, Dict, Any
from datetime import datetime



class Player:
    # dictionnary of field_name: field description to create a new Player
    INPUT_FIELDS = {
        'first_name': "Player's first name",
        'last_name': "Player's last name",
        'birthday': "Player's birthday DD/MM/YYYY",
        'club_id': "Player's club id",
    }

    def __init__(self,id:int,first_name: str, last_name: str, birthday: datetime, club_id: str = "AB12345"):
        self.score = 0
        self.id = id or 1
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.club_id = club_id

    @classmethod
    def from_values(cls, values: Dict[str, Any]):
        birthday = datetime.strptime(values['birthday'], "%d/%m/%Y")
        user_id = values['id']
        return cls(
            id=user_id,
            first_name=values['first_name'],
            last_name=values['last_name'],
            birthday=birthday,
            club_id=values['club_id']
        )

    def as_dict(self):
        player ={       "id":self.id,
                        "first name": self.first_name,
                        "last name": self.last_name,
                        "birthday DD/MM/YYYY": self.birthday,
                        "club id": self.club_id
        }
        return player

    def get_player_with_score(self):
        player_with_score = {
            "player :": self.as_dict(),
            "score :": self.score
        }
        return player_with_score


class Match:
    def __init__(self, player_a: Player, player_b: Player):
        self.player_a = player_a
        self.player_b = player_b
        self.result = None

    def get_match(self, round):
        self.round = round
        match = {
            "round :": self.round,
            "Player A :": self.player_a,
            "Player B :": self.player_b,
            "Result :": self.result
        }
        return match


class Tournament:
    def __init__(self, id: int, name: str, location: str, start_date: datetime, end_date: datetime, number_round: int,
                 description: str, total_number_round: int, player_id: list = None):
        self.id = id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_round = number_round
        self.description = description
        self.total_number_round = total_number_round
        self.players = player_id  # WARNING fixme

        self.current_round = 1
        self.current_round_matches = []
        self.rounds = []
        self.players_scores = {}

    def get_tournament(self):
        tournament = {
            "Name": self.name,
            "Location": self.location,
            "First match date DD/MM/YYYY": self.start_date,
            "Last match date DD/MM/YYYY": self.end_date,
            "Total number of round": self.total_number_round,
            "Round": self.number_round,
            "List of players participate": self.players,
            "Descrition of the tournament": self.description
        }
        return tournament

    def is_finished(self):
        now = datetime.now()
        return self.end_date <= now

    def start(self):
        self.current_round_matches = self.generate_first_round_match_pairs()
        self.players_scores = ...

    def go_to_next_round(self):
        self.rounds.append(self.current_round_matches)
        self.current_round += 1
        self.current_round_matches = self.generate_round_match_pairs()

    def generate_first_round_match_pairs(self):

        random.shuffle(self.players)
        if (len(self.players)) % 2 == 0:
            list_temporary = [self.players[i:i + 2] for i in range(0, len(self.players), 2)]
            list_player_opponent_round = {1: list_temporary}
            return list_player_opponent_round
        else:
            list_temporary = [self.players[i:i + 2] for i in range(0, len(self.players) - 1, 2)]
            list_temporary.append([self.players[-1], None])
            list_player_opponent_round = {"1": list_temporary}
            return list_player_opponent_round

    def generate_round_match_pairs(self):
        pass
