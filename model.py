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
            club_id=document['club id'],

        )

    def as_dict(self):
        player = {
            "id": self.id,
            "first name": self.first_name,
            "last name": self.last_name,
            "birthday DD/MM/YYYY": self.birthday,
            "club id": self.club_id,
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

    def as_match(self):
        match = {
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

    def __init__(self, name: str, location: str, start_date: datetime, end_date: datetime,
                 description: str, total_number_round: int, players: list = None):
        # self.ids = ids
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.current_round_number: int = 1
        self.total_number_round = total_number_round
        self.players: List[Player] = players
        # initialiser la map avec les identifiants des joueurs, regarder la fonction dict.from_keys() ou quelque chose du genre
        self.players_scores: Dict[int, float] = {player[0]['id']: 0 for player in  # player[0]['id']
                                                 self.players}  # map of player id: score in the tournament
        self.player_ids: List[int] = [player[0]['id'] for player in self.players]
        self.total_match = []
        self.match_in_round: Dict[int, [Match]] = {self.current_round_number: []}
        self.round_time_start: [Dict[int, str]] = {self.current_round_number: ''}
        self.round_time_end: [Dict[int, str]] = {self.current_round_number: ''}

    # def __str__(self):
    #     return f"Tournament: name={self.name}, location={self.location}, start_date={self.start_date}, end_date={self.end_date}, players={self.players}, rounds={self.number_round}"

    @classmethod
    def from_values(cls, values: Dict[str, Any]) -> 'Tournament':
        start_date = datetime.strptime(values['start date'], "%d/%m/%Y")
        end_date = datetime.strptime(values['end date'], "%d/%m/%Y")
        # tournament_id = values['id']
        players = values['player']
        return cls(
            # ids = tournament_id,
            name=values['name'],
            location=values['location'],
            start_date=start_date,
            end_date=end_date,
            description=values['tournament description'],
            total_number_round=4,
            players=players,
        )

    @classmethod
    def from_db(cls, document: Dict[str, Any]) -> 'Tournament':  # players: Dict[int, Player]
        # start_date = datetime.strftime(document['start_date'], "%d/%m/%Y")
        # end_date = datetime.strftime(document['end_date'], "%d/%m/%Y")

        return cls(

            name=document['Name'],
            location=document['Location'],
            start_date=document['start_date'],
            end_date=document['end_date'],
            # current_round_number=document['current round number'],
            description=document['description'],
            total_number_round=document['total round of tournament'],
            players=document['players in tournament'],
            # players_scores=document['player scores']
        )

    def to_db(self):
        # TODO à remplir, le but est d'avoir une structure pour la DB et pas pour l'affichage.
        # À lier avec la fonction from_db pour les clefs de document
        json_data = {
            'player_ids': self.player_ids,
            'Name': self.name,
            'Location': self.location,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'description': self.description,
            'total round of tournament': self.total_number_round,
            'players in tournament': self.players,
            'current round number': self.current_round_number,
            'player scores': self.players_scores,
            'total match': self.total_match,
            'match by round': self.match_in_round,
            'round start time':self.round_time_start,
            'round end time':self.round_time_end,
        }
        return json_data

    def as_dict(self):
        tournament = {
            # 'tournament id':self.ids,
            "Name": self.name,
            "Location": self.location,
            "First match date DD/MM/YYYY": self.start_date,
            "Last match date DD/MM/YYYY": self.end_date,
            "Total number of round": self.total_number_round,
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
        # TODO m'appeler depuis le controller
        # self.current_round += 1
        # new_round: Round = self.generate_next_round()
        # self.rounds.append(new_round)
        # if self.current_round == self.number_round
        self.generate_next_round()

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
                name_player1 = match.as_match().get("Player A :")[0].get("first name") + " " + \
                               match.as_match().get("Player A :")[0].get("last name")
                name_player2 = match.as_match().get("Player B :")[0].get("first name") + " " + \
                               match.as_match().get("Player B :")[0].get("last name")
                print(f'Match {match_number} : {name_player1} VS {name_player2}\n')
                match_number += 1
                i += 2
        else:
            print(f'The number of the players must be even')
        # print(list_match_round_one)
        new_dict = {self.current_round_number: current_round_matchs}
        self.match_in_round.update(new_dict)
        round_start_time = datetime.strftime(datetime.now(), "%d/%m/%Y")
        self.round_time_start.update({self.current_round_number: round_start_time})
        self.start_date = datetime.now()
        print(self.round_time_start)
        # print(self.players)

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
            print(f'the match state changed')
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
        round_end_time = datetime.strftime(datetime.now(), "%d/%m/%Y")
        self.round_time_end.update({self.current_round_number: round_end_time})
        self.sort_list_of_players_by_scores()

    def sort_list_of_players_by_scores(self):
        list_sorted = dict(sorted(self.players_scores.items(), key=lambda score: score[1], reverse=True))
        print(f'The player list sorted by score is done')
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
        current_round_matchs = []
        list_next_round = self.players.copy()
        print(list_next_round)
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
            round_start_time = datetime.strftime(datetime.now(), "%d/%m/%Y")
            self.round_time_start.update({self.current_round_number: round_start_time})
            self.current_round_number += 1
            print(self.round_time_start)
        else:
            print('It\'s not possible to distribute match,Match is finished!')
            self.end_date = datetime.now
        # print(self.match_in_round)
        # for match in self.total_match:
        #     print(match.as_match())
        # print(f'the pair list for next round {current_round_matchs}\n')
        # print(f'The paired player list {self.total_match}')
