class Player():
    def __init__(self, id=1, first_name="", last_name="", birthday=19900203, club_id="AB12345"):
        self.id = id or 1
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.club_id = club_id

    def dict_player(self):
        player = {
            "Player's id" : self.id,
        "Player's first name" : self.first_name,
        "Player's last name" : self.last_name,
        "Player's birthday DD/MM/YYYY" : self.birthday,
        "Player's club id" : self.club_id
        }
        return player

class match():
    def __init__(self,player_a:Player,player_b:Player):
        self.player_a = player_a
        self.player_b = player_b
        self.reslutat = None
    def dict_math(self):
        match = {
            "Player A":self.player_a,
            "Player B":self.player_b
        }
        return match

class Tournament():
    def __init__(self, name="", location="", date_action=0, date_finish=1, number_round=1, players="", description="",
                 total_number_round=4):
        self.players = []
        self.name = name
        self.location = location
        self.date_action = date_action
        self.date_finish = date_finish
        self.number_round = number_round
        for player in players:
            self.players.append(player)
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
