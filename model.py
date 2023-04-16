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
    INPUT_FIELDS = {
        'name': "tournament name",
        'location': "tournament location",
        'start date': "tournament starting date DD/MM/YYYY",
        'end date': "tournament ending date DD/MM/YYYY",
        'tournament description': "tournament description",
        'total round number': "total tournaments round number,4 by default",
    }

    def __init__(self, name: str, location: str, start_date: datetime, end_date: datetime, number_round: int,
                 description: str, total_number_round: int, player: list = None):
        # self.ids = ids
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_round = number_round
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
            number_round=0,
            description=values['tournament description'],
            total_number_round=4,
            player=player,
        )

    @classmethod
    def from_db(cls, document: Dict[str, Any]):
        # start_date = datetime.strftime(document['First match date DD/MM/YYYY'], "%d/%m/%Y")
        # end_date = datetime.strptime(document['Last match date DD/MM/YYYY'], "%d/%m/%Y")
        return cls(
            # ids=document['tournament id'],
            name=document['Name'],
            location=document['Location'],
            start_date=document['First match date DD/MM/YYYY'],
            end_date=document['Last match date DD/MM/YYYY'],
            number_round=0,
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
    def generate_random_opponent_first_match(list_contestants):
        """
        for the first round game,we use random function
        :param list_contestants: a list of contestants for the tournaments
        :return: a dictionary key = round information value = list every opponents
        """

        random.shuffle(list_contestants)
        if (len(list_contestants)) % 2 == 0:
            list_temporary = [list_contestants[i:i + 2] for i in range(0, len(list_contestants), 2)]
            list_player_opponent = list_temporary

        else:
            list_temporary = [list_contestants[i:i + 2] for i in range(0, len(list_contestants) - 1, 2)]
            list_temporary.append([list_contestants[-1], None])
            list_player_opponent = list_temporary

        return list_player_opponent

    @staticmethod
    def update_winner_state_match(total_list_paired: list[str], db,dict_player_with_score:list or None):
        """
        :param list_opponent_in_match: a list contains [every opponents information] in a round
        :param rounds: round number
        :return: a list contain two list,list one[opponents information],two [winner],list_opponent_in_match is a dict
                 contains round number and list player in match with winner
        """
        players = db
        dict_player_with_score = {}
        score_initial = 0


        for list_paired in total_list_paired:
            player1 = players.get(int(list_paired[0]))
            player2 = players.get(int(list_paired[1]))
            player1_name = player1.first_name + " " + player1.last_name
            player2_name = player2.first_name + " " + player2.last_name
            choice = input(f'The winner is 1 for {player1_name}, 2 for {player2_name}, or 3 for Draw\n')
            if choice == '1':
                score = score_initial + 1
                new_dict = {list_paired[0]: score}
                dict_player_with_score.update(new_dict)
                new_dict = {list_paired[1]: score_initial}
                dict_player_with_score.update(new_dict)
            elif choice == '2':
                score = score_initial + 1
                new_dict = {list_paired[1]: score}
                dict_player_with_score.update(new_dict)
                new_dict = {list_paired[0]: score_initial}
                dict_player_with_score.update(new_dict)
            else:
                score = score_initial + 0.5
                new_dict = {list_paired[0]: score}
                dict_player_with_score.update(new_dict)
                new_dict = {list_paired[1]: score}
                dict_player_with_score.update(new_dict)
        return dict_player_with_score

    @staticmethod
    def sort_list_of_players_by_scores(list_player_with_score):
        list_player_sorted_by_scores = dict(
            sorted(list_player_with_score.items(), key=lambda score: score[1], reverse=True))
        return list_player_sorted_by_scores

    @staticmethod
    def generate_next_round_match(list_next_round, list_total):
        all_paire_possibilite = []
        j = 1
        r = 1
        while j <= len(list_next_round) - 1:
            paire = [list_next_round[0], list_next_round[j]]
            print(paire)
            if paire != [] and paire not in list_total and paire[::-1] not in list_total:
                all_paire_possibilite.append(paire)
                list_total.append(paire)
                list_next_round.remove(list_next_round[0])
                list_next_round.remove(list_next_round[j - 1])
                print(list_next_round)
                print(list_total)
                j = 1
            else:
                j += 1
            r += 1
            print(f'the {r} try')
        if not len(all_paire_possibilite):
            print('No match can be distributed')

        print(all_paire_possibilite)
        print(list_total)

        return all_paire_possibilite, list_total
