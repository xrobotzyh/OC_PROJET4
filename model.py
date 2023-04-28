import random
from typing import List, Dict, Any, Optional
from datetime import datetime

DATETIME_FORMAT = "%d/%m/%Y"


class Player:
    # dictionnary of field_name: field description to create a new Player
    INPUT_FIELDS = {
        'first_name': "Player's first name",
        'last_name': "Player's last name",
        'birthday': "Player's birthday DD/MM/YYYY",
        'club_id': "Player's club id",
    }

    def __init__(self, id: int, first_name: str, last_name: str, birthday: datetime, club_id: str = "AB12345"):
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

    def to_json(self):
        birthday = datetime.strftime(self.birthday, DATETIME_FORMAT)
        player = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": birthday,
            "club_id": self.club_id,
        }
        return player

    @classmethod
    def from_json(cls, document: Dict[str, Any]):
        birthday = datetime.strptime(document['birthday'], DATETIME_FORMAT)
        return cls(
            id=document['id'],
            first_name=document['first_name'],
            last_name=document['last_name'],
            birthday=birthday,
            club_id=document['club_id'],
        )

    def __str__(self) -> str:
        return f"{self.id}: {self.first_name} {self.last_name} ({self.club_id})"


class Match:
    def __init__(self, player_a: Player, player_b: Player, result: Optional[int] = None):
        self.player_a = [player_a, 0]
        self.player_b = [player_b, 0]
        self.result = result

    def set_result(self, result):
        if result == '1':
            self.player_a[1] = 1
        elif result == '2':
            self.player_b[1] = 1
        elif result == '3':
            self.player_a[1] = 0.5
            self.player_b[1] = 0.5

    def __str__(self):
        return f"player A: {str(self.player_a[0])} VS player B: {str(self.player_b[0])} "

    def to_json(self):
        # ODO
        return {
            "player_a": [self.player_a[0].id, self.player_a[1]],
            "player_b": [self.player_b[0].id, self.player_b[1]],
            "result": self.result
        }

    @classmethod
    def from_json(cls, document, players: List[Player]):
        for player in players:
            if player.id == document["player_a"][0]:
                player_a = player
            if player.id == document["player_b"][0]:
                player_b = player
        return cls(
            player_a=player_a,
            player_b=player_b,
            result=document['result']
        )


class Round:
    def __init__(self, matches: List[Match], name: str):
        self.matches: List[Match] = matches
        self.name = name
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def start(self):
        self.start_time = datetime.now()

    def close(self):
        self.end_time = datetime.now()

    def to_json(self) -> Dict[str, Any]:
        # ODO
        if type(self.start_time) == datetime:
            start_time = datetime.strftime(self.start_time, DATETIME_FORMAT)
        else:
            start_time = self.start_time
        if self.end_time is not None and type(self.start_time) == datetime:
            end_time = datetime.strftime(self.end_time, DATETIME_FORMAT)
        else:
            end_time = self.end_time
        return {
            'list_of_match': [match.to_json() for match in self.matches],
            'round_name': self.name,
            'round_start_time': start_time,
            'round_end_time': end_time,
        }

    @classmethod
    def from_json(cls, document, players_db: Dict[int, Player]) -> 'Round':
        # ODO
        players = []
        matches = []
        for player in players_db.values():
            players.append(player)
        for json_match in document['list_of_match']:
            match = Match.from_json(json_match, players)
            matches.append(match)

        round = cls(
            matches=matches,
            name=document['round_name'],
        )
        round.start_time = document['round_start_time']
        round.end_time = document['round_end_time']

        return round


class Tournament:
    INPUT_FIELDS = {
        'name': "tournament name",
        'location': "tournament location",
        'start date': "tournament starting date DD/MM/YYYY",
        'end date': "tournament ending date DD/MM/YYYY",
        'tournament description': "tournament description",
        'total round number': "total tournaments round number,4 by default",
    }

    def __init__(self,
                 name: str,
                 location: str,
                 start_date: datetime,
                 end_date: datetime,
                 description: str,
                 players: List[Player],
                 total_round_number: int = 4):
        # self.ids = ids
        # create a new tournament from scratch
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.current_round_number = 1
        self.total_round_number = total_round_number
        self.players: List[Player] = players
        self.players_scores: Dict[int, float] = {player.id: 0 for player in players}
        self.rounds: List[Round] = []

    def __str__(self):
        return f'{self.name} in {self.location} at {self.start_date} and end in {self.end_date},the current round is' \
               f'{self.current_round_number} and players is {[str(player) for player in self.players]}'

    @classmethod
    def from_values(cls, values: Dict[str, Any]) -> 'Tournament':
        start_date = datetime.strptime(values['start date'], DATETIME_FORMAT)
        end_date = datetime.strptime(values['end date'], DATETIME_FORMAT)
        # tournament_id = values['id']
        players = values['players']
        return cls(
            # ids = tournament_id,
            name=values['name'],
            location=values['location'],
            start_date=start_date,
            end_date=end_date,
            description=values['tournament description'],
            total_round_number=4,
            players=players,
        )

    @classmethod
    def from_json(cls, document: Dict[str, Any], players_db: Dict[int, Player]) -> 'Tournament':
        # De-serialize the JSON in a Tournament data structure

        # Get player's list using the players database and the ids list stored in the json
        player_ids: List[int] = document['player_ids']
        players: List[Player] = []
        for player_id in player_ids:
            player: Player = players_db[player_id]
            players.append(player)

        tournament = cls(
            name=document['name'],
            location=document['location'],
            start_date=datetime.strptime(document['start_date'], DATETIME_FORMAT),
            end_date=datetime.strptime(document['end_date'], DATETIME_FORMAT),
            description=document['description'],
            total_round_number=document['total_round_number'],
            players=players,
        )
        tournament.players_scores = document['players_scores']
        tournament.current_round_number = document['current_round_number']
        rounds = []
        for json_round in document['rounds']:
            round = Round.from_json(json_round, players_db)
            rounds.append(round)
        tournament.rounds = rounds
        return tournament

    def to_json(self):
        # Serialize the tournament in a JSON format
        json_data = {
            'name': self.name,
            'location': self.location,
            'start_date': datetime.strftime(self.start_date, DATETIME_FORMAT),
            'end_date': datetime.strftime(self.end_date, DATETIME_FORMAT),
            'description': self.description,
            'current_round_number': self.current_round_number,
            'total_round_number': self.total_round_number,
            'players_scores': {player.id: 0 for player in self.players},
            'player_ids': [player.id for player in self.players],
            'rounds': [round.to_json() for round in self.rounds],
        }
        return json_data

    def as_dict(self):
        tournament = {
            # 'tournament id':self.ids,
            "Name": self.name,
            "Location": self.location,
            "First match date DD/MM/YYYY": self.start_date,
            "Last match date DD/MM/YYYY": self.end_date,
            "Total number of round": self.total_round_number,
            "current round number": self.current_round_number,
            "List of players participate": [str(player) for player in self.players],
            "Description of the tournament": self.description
        }
        return tournament

    def is_finished(self):
        now = datetime.now()
        return self.end_date <= now

    def start(self):
        self.generate_first_round()
        # self.update_winner_state_match()
        # new_round: Round = self.generate_first_round()
        # self.rounds.append(new_round)
        # self.players_scores =

    def go_to_next_round(self):
        current_round = self.rounds[-1]
        # current_round.close()
        if self.current_round_number == self.total_round_number:
            self.finish()
        else:
            self.generate_next_round()

    def finish(self):
        self.end_date = datetime.strftime(datetime.now(), DATETIME_FORMAT)

    def generate_first_round(self):
        """
        for the first round game,we use random function
        :param list_contestants: a list of contestants for the tournaments
        :return: a dictionary key = round information value = list every opponents
        """
        match_number = 1
        list_matches = []
        round_name = 'round' + ' ' + str(self.current_round_number)
        print(round_name)
        random.shuffle(self.players)
        if (len(self.players)) % 2 == 0:
            i = 0
            while i < len(self.players):
                match = Match(self.players[i], self.players[i + 1])
                list_matches.append(match)
                print(f'Match {match_number}: {match}')
                i += 2
                match_number += 1
        else:
            print('The number of the players must be even')
        # print(list_match_round_one)
        current_round = Round(list_matches, round_name)
        current_round.start()
        self.rounds.append(current_round)
        # print(self.rounds[0].to_json())

    def get_current_round_details(self) -> str:
        pass

    def sort_list_of_players_by_scores(self):
        list_sorted = dict(sorted(self.players_scores.items(), key=lambda score: score[1], reverse=True))
        print('The player list sorted by score is done')
        self.players_scores = list_sorted
        sorted_players = []
        for player_id in list_sorted.keys():
            for player in self.players:
                if str(player.id) == player_id:
                    sorted_players.append(player)
        self.players = sorted_players

    def generate_next_round(self):
        current_round_matches = []
        list_next_round = self.players.copy()
        round_name = 'round' + ' ' + str(self.current_round_number)
        print(round_name)
        i = 1
        j = 0
        match_number = 0
        total_matches = []
        while j < self.current_round_number - 1:
            for match in self.rounds[j].matches:
                total_matches.append([match.player_a[0], match.player_b[0]])
            j += 1
        while i <= len(list_next_round) - 1:
            match = Match(list_next_round[0], list_next_round[i])
            if match != [] and [match.player_a[0], match.player_b[0]] not in total_matches and \
                    [match.player_b[0], match.player_a[0]] not in total_matches:
                match_number += 1
                current_round_matches.append(match)
                list_next_round.remove(list_next_round[0])
                list_next_round.remove(list_next_round[i - 1])
                print(f'Match {match_number} :  {match.player_a[0]} VS {match.player_b[0]}\n')
                i = 1
            else:
                i += 1
        if not len(list_next_round):
            print('All matches distributed')
        if current_round_matches is not None:
            # if current round match information is not None, create a round and start time information to db
            current_round = Round(current_round_matches, round_name)
            current_round.start()
            self.rounds.append(current_round)
        else:
            print('It\'s not possible to distribute match.')

    def update_players_scores(self):
        round = self.rounds[-1]
        for match in round.matches:
            player_a_id = match.player_a[0].id
            player_b_id = match.player_b[0].id
            score_a = self.players_scores.get(player_a_id) + match.player_a[1]
            score_b = self.players_scores.get(player_b_id) + match.player_b[1]
            self.players_scores.update({player_a_id: score_a})
            self.players_scores.update({player_b_id: score_b})
        print(self.players_scores)
