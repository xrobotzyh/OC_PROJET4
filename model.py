import random
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

    @classmethod
    def from_db(cls, document: Dict[str, Any]):
        birthday = document['birthday DD/MM/YYYY']  # datetime.strptime(, "%d/%m/%Y")
        return cls(
            id=document['id'],
            first_name=document['first name'],
            last_name=document['last name'],
            birthday=birthday,
            club_id=document['club id']
        )

    def as_dict(self):
        player = {
            "id": self.id,
            "first name": self.first_name,
            "last name": self.last_name,
            "birthday DD/MM/YYYY": self.birthday,
            "club id": self.club_id
        }
        return player



class Match:
    def __init__(self, player_a: Player, player_b: Player):
        self.match_round = None
        self.player_a = player_a
        self.player_b = player_b
        self.result = None

    def as_match(self, match_round):
        self.match_round = match_round
        match = {
            "round :": self.match_round,
            "Player A :": self.player_a,
            "Player B :": self.player_b,
            "Result :": self.result
        }
        return match



class Tournament:
    INPUT_FIELDS = {
        'name': "tournament name",
        'location': "tournament location",
        'start date': "tournament starting date DD/MM/YYYY",
        'end date': "tournament ending date DD/MM/YYYY",
        'tournament description': "tournament description",
        'total round number': "total tournaments round number,4 by default",
    }

    def __init__(self, name: str, location: str, start_date: datetime, end_date: datetime, round_number: int,
                 description: str, total_number_round: int, player: list = None):
        # self.ids = ids
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_round = round_number
        self.description = description
        self.total_number_round = total_number_round
        self.players = player

        # self.current_round = 0
        # self.current_round_matches = []
        # self.rounds = []
        # self.players_scores = {}

    def __str__(self):
        return f"Tournament: name={self.name}, location={self.location}, start_date={self.start_date}, end_date={self.end_date}, players={self.players}, rounds={self.number_round}"

    @classmethod
    def from_values(cls, values: Dict[str, Any]):
        start_date = datetime.strptime(values['start date'], "%d/%m/%Y")
        end_date = datetime.strptime(values['end date'], "%d/%m/%Y")
        # tournament_id = values['id']
        player = values['player']
        return cls(
            # ids = tournament_id,
            name=values['name'],
            location=values['location'],
            start_date=start_date,
            end_date=end_date,
            round_number=0,
            description=values['tournament description'],
            total_number_round=4,
            player=player,
        )

    @classmethod
    def from_db(cls, document: Dict[str, Any]):
        start_date = datetime.strftime(document['First match date DD/MM/YYYY'], "%d/%m/%Y")
        end_date = datetime.strftime(document['Last match date DD/MM/YYYY'], "%d/%m/%Y")
        return cls(
            # ids=document['tournament id'],
            name=document['Name'],
            location=document['Location'],
            start_date=start_date,
            end_date=end_date,
            round_number=0,
            description=document['Descrition of the tournament'],
            total_number_round=4,
            player=document['List of players participate'],
        )

    def as_dict(self):
        tournament = {
            # 'tournament id':self.ids,
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

    @staticmethod
    def is_finished(end_date):
        now = datetime.now()
        return end_date <= now

    def start(self):
        self.current_round_matches = self.generate_random_opponent_first_match()
        self.players_scores = ...

    def go_to_next_round(self):
        self.rounds.append(self.current_round_matches)
        self.current_round += 1
        self.current_round_matches = self.generate_round_match_pairs()

    @staticmethod
    def generate_random_opponent_first_match(list_players):
        """
        for the first round game,we use random function
        :param list_contestants: a list of contestants for the tournaments
        :return: a dictionary key = round information value = list every opponents
        """
        list_match_round_one = []
        list_match_current_round = []

        random.shuffle(list_players)
        if (len(list_players)) % 2 == 0:
            i = 0
            while i <= len(list_players) // 2:
                match = Match(list_players[i], list_players[i + 1])
                list_match_round_one.append(match)
                list_match_current_round.append([match.player_a, match.player_b])
                print(f'***pair successful{[list_players[i], list_players[i + 1]]}***\nThe paired player list')
                print(list_match_current_round)
                i += 2
        else:
            print(f'The number of the players must be even')
        # print(list_match_round_one)
        return list_match_round_one

    @staticmethod
    def update_winner_state_match(list_match_round_x: list[Match], db, player_with_score: dict[int:int]):
        """
        :param list_opponent_in_match: a list contains [every opponents information] in a round
        :param rounds: round number
        :return: a list contain two list,list one[opponents information],two [winner],list_opponent_in_match is a dict
                 contains round number and list player in match with winner
        """
        players = db

        for match in list_match_round_x:
            player1 = players.get(match.player_a)
            player2 = players.get(match.player_b)
            player1_name = player1.first_name + " " + player1.last_name
            player2_name = player2.first_name + " " + player2.last_name
            match.result = input(f'The winner is 1 for {player1_name}, 2 for {player2_name}, or 3 for tie\n')
            print(f'the match state changed')
            print(f'{match.as_match(1)}\n')
            if match.result == '1':
                score = player_with_score[player1.id] + 1
                new_dict = {player1.id: score}
                player_with_score.update(new_dict)

            elif match.result == '2':
                score = player_with_score[player2.id] + 1
                new_dict = {player2.id: score}
                player_with_score.update(new_dict)
            else:
                score = player_with_score[player1.id] + 0.5
                new_dict = {player1.id: score}
                player_with_score.update(new_dict)
                score = player_with_score[player2.id] + 0.5
                new_dict = {player2.id: score}
                player_with_score.update(new_dict)
            print(f'The list of player before sort by score')
            print(f'{player_with_score}\n')

        return player_with_score

    @staticmethod
    def sort_list_of_players_by_scores(list_player_with_score):
        list_player_sorted_by_scores = dict(
            sorted(list_player_with_score.items(), key=lambda score: score[1], reverse=True))
        print(f'The player list sorted by score is done')
        print(f'{list_player_sorted_by_scores}\n')
        return list_player_sorted_by_scores

    @staticmethod
    def generate_next_round_match(list_next_round, list_total):
        all_match = []
        list_match_current_round = []
        j = 1
        r = 1
        while j <= len(list_next_round) - 1:
            match = Match(list_next_round[0], list_next_round[j])  # TypeError: 'type' object is not subscriptable
            print(match.as_match(2))
            if match != [] and [match.player_a, match.player_b] not in list_total and [match.player_b,
                                                                                       match.player_a] not in list_total:
                all_match.append(match)
                list_total.append([match.player_a, match.player_b])
                list_match_current_round.append([match.player_a, match.player_b])
                list_next_round.remove(match.player_a)
                list_next_round.remove(match.player_b)
                print(f'***pair successful : {[match.player_a, match.player_b]}***\n')
                # print(f'The paired player list {list_total}\n')
                j = 1
            else:
                j += 1
            # r += 1
            # print(f'the {r} try')
        if not len(all_match):
            print('No match can be distributed')

        print(f'the pair list for next round {list_match_current_round}\n')
        print(f'The paired player list {list_total}')

        return all_match, list_total
