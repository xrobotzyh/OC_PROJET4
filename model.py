from typing import List
from datetime import datetime

class Player():
    def __init__(self, id:int, first_name:str, last_name:str, birthday:datetime, club_id:str= "AB12345"):
        self.score = 0
        self.id = id or 1
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.club_id = club_id

    def get_player(self):
        player = {
            "Player's id" : self.id,
        "Player's first name" : self.first_name,
        "Player's last name" : self.last_name,
        "Player's birthday DD/MM/YYYY" : self.birthday,
        "Player's club id" : self.club_id
        }
        return player

    def get_player_with_score(self):
        player_with_score = {
            "player :":self.get_player(),
            "score :":self.score
        }
        return player_with_score

class Match:
    def __init__(self,player_a:Player,player_b:Player):
        self.player_a = player_a
        self.player_b = player_b
        self.result = None
    def get_match(self,round):
        self.round = round
        match = {
            "round :":self.round,
            "Player A :":self.player_a,
            "Player B :":self.player_b,
            "Result :":self.result
        }
        return match

class Tournament():
    def __init__(self, name:str, location:str, start_date:datetime, end_date:datetime, number_round:int,
                 description:str, total_number_round:int, player_id:list=None):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_round = number_round
        self.description = description
        self.total_number_round = total_number_round
        self.players = player_id
        
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
