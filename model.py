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

    def to_json(self):
        player = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birthday": self.birthday,
            "club_id": self.club_id,
        }
        return player


class Match:
    def __init__(self, player_a: Player, player_b: Player, result: Optional[int] = None):
        self.player_a = [player_a, 0]
        self.player_b = [player_b, 0]

    def set_result(self, result: int):
        if result == 1:
            self.player_a[1] = 1
        elif result == 2:
            self.player_b[1] = 1
        elif result == 3:
            self.player_a[1] = 0.5
            self.player_b[1] = 0.5

    def __str__(self):
        return f"{self.player_a[0].first_name} {self.player_a[0].last_name} ({self.player_a[1]}) " \
               f"- {self.player_b[0].first_name} {self.player_b[0].last_name} ({self.player_b[1]})"

    def to_json(self):
        # TODO
        return {}

    @classmethod
    def from_json(cls, values):
        # TODO
        return None


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
        # TODO
        return {}

    @classmethod
    def from_json(cls, values, players_db: Dict[int, Player]) -> 'Round':
        # TODO
        return None


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
        self.players_scores: Dict[int, float] = {player.id: 0 for player in players}
        self.players: List[Player] = players
        self.rounds: List[Round] = []

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
            'players_scores': self.players_scores,
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
            "List of players participate": self.players,
            "Description of the tournament": self.description
        }
        return tournament

    def is_finished(self):
        now = datetime.now()
        return self.end_date <= now

    def start(self):
        self.generate_first_round()
        self.current_round_number += 1
        # self.update_winner_state_match()
        # self.sort_list_of_players_by_scores()

        # new_round: Round = self.generate_first_round()
        # self.rounds.append(new_round)
        # self.players_scores =

    def go_to_next_round(self):
        current_round = self.rounds[-1]
        self.update_players_scores(current_round)
        current_round.close()
        if self.current_round_number == self.total_round_number:
            return
        else:
            self.generate_next_round()

        # TODO m'appeler depuis le controller
        # new_round: Round = self.generate_next_round()
        # self.rounds.append(new_round)
        #

    def generate_first_round(self):
        """
        for the first round game,we use random function
        :param list_contestants: a list of contestants for the tournaments
        :return: a dictionary key = round information value = list every opponents
        """

        current_round_matchs = []

        random.shuffle(self.players)
        if (len(self.players)) % 2 == 0:
            i = 0
            match_number = 1
            while i < len(self.players):
                match = Match(self.players[i], self.players[i + 1])
                current_round_matchs.append(match)
                self.total_match.append([match.player_a, match.player_b])
                # name_player1 = match.as_match().get("Player A :")[0].get("first name") + " " + \
                #                match.as_match().get("Player A :")[0].get("last name")
                # name_player2 = match.as_match().get("Player B :")[0].get("first name") + " " + \
                #                match.as_match().get("Player B :")[0].get("last name")
                # print(f'Match {match_number} : {name_player1} VS {name_player2}\n')
                match_number += 1
                i += 2
        else:
            print('The number of the players must be even')
        # print(list_match_round_one)
        new_dict = {self.current_round_number: current_round_matchs}
        self.match_in_round.update(new_dict)
        round_start_time = datetime.strftime(datetime.now(), DATETIME_FORMAT)
        self.round_time_start.update({self.current_round_number: round_start_time})
        # self.start_date = datetime.now()
        print(self.round_time_start)
        # print(self.players)

    def get_current_round_details(self) -> str:
        pass

    def update_winner_state_match(self):
        """
        :param list_opponent_in_match: a list contains [every opponents information] in a round
        :param rounds: round number
        :return: a list contain two list,list one[opponents information],two [winner],list_opponent_in_match is a dict
                 contains round number and list player in match with winner
        """
        round_number = self.current_round_number - 1
        current_round_matchs = self.match_in_round[round_number]
        for match in current_round_matchs:
            name_player1 = match.as_match().get("Player A :")[0].get("first name") + " " + \
                           match.as_match().get("Player A :")[0].get("last name")
            name_player2 = match.as_match().get("Player B :")[0].get("first name") + " " + \
                           match.as_match().get("Player B :")[0].get("last name")
            match.result = input(f'The winner is 1 for {name_player1}, 2 for {name_player2}, or 3 for tie\n')
            print('the match state changed')
            if match.result == '1':
                player_id = match.player_a[0].get('id')
                score = self.players_scores[player_id] + 1
                new_dict = {player_id: score}
                self.players_scores.update(new_dict)
            elif match.result == '2':
                player_id = match.player_b[0].get('id')
                score = self.players_scores[player_id] + 1
                new_dict = {player_id: score}
                self.players_scores.update(new_dict)
            else:
                player_id = match.player_a[0].get('id')
                score = self.players_scores[player_id] + 0.5
                new_dict = {player_id: score}
                self.players_scores.update(new_dict)
                player_id = match.player_b[0].get('id')
                score = self.players_scores[player_id] + 0.5
                new_dict = {player_id: score}
                self.players_scores.update(new_dict)
            # print(f'The list of player before sort by score')
            # print(f'{self.players_scores}\n')
        round_end_time = datetime.strftime(datetime.now(), DATETIME_FORMAT)
        self.round_time_end.update({self.current_round_number: round_end_time})
        self.sort_list_of_players_by_scores()

    def sort_list_of_players_by_scores(self):
        list_sorted = dict(sorted(self.players_scores.items(), key=lambda score: score[1], reverse=True))
        print('The player list sorted by score is done')
        self.players_scores = list_sorted
        sorted_players = []
        for player_id in list_sorted.keys():
            for player in self.players:
                if player[0]['id'] == player_id:
                    sorted_players.append(player)
        self.players = sorted_players
        print(f'{self.players_scores}')
        # print(f'{self.players}')

    def generate_next_round(self):
        self.current_round_number += 1
        current_round_matchs = []
        list_next_round = self.players.copy()
        # print(list_next_round)
        i = 1
        match_number = 0
        while i <= len(list_next_round) - 1:
            match = Match(list_next_round[0], list_next_round[i])
            if match != [] and [match.player_a, match.player_b] not in self.total_match and [match.player_b,
                                                                                             match.player_a] not in self.total_match:

                match_number += 1
                current_round_matchs.append(match)
                self.total_match.append([match.player_a, match.player_b])
                list_next_round.remove(match.player_a)
                list_next_round.remove(match.player_b)
                name_player1 = match.player_a[0].get("first name") + " " + \
                               match.as_match().get("Player A :")[0].get("last name")
                name_player2 = match.as_match().get("Player B :")[0].get("first name") + " " + \
                               match.as_match().get("Player B :")[0].get("last name")
                print(f'Match {match_number} :  {name_player1} VS {name_player2}\n')
                i = 1
            else:
                i += 1
        if not len(list_next_round):
            print('All matches distributed')
        if current_round_matchs:
            new_dict = {self.current_round_number: current_round_matchs}
            self.match_in_round.update(new_dict)
            round_start_time = datetime.strftime(datetime.now(), DATETIME_FORMAT)
            self.round_time_start.update({self.current_round_number: round_start_time})
            self.current_round_number += 1
            print(self.round_time_start)
        else:
            print('It\'s not possible to distribute match,Match is finished!')
            # self.end_date = datetime.now
        # print(self.total_match)
        # print(f'************')
        #
        # print(len(matchs_in_round))
        # print(matchs_in_round)

        # for match in self.total_match:
        #     print(match.as_match())
        # print(f'the pair list for next round {current_round_matchs}\n')
        # print(f'The paired player list {self.total_match}')
