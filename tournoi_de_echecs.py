import random


class Players:
    '''
        a class that contains all the players informations and can calculate the scores after each round
        of the games
    '''
    def __init__(self,first_name,last_name,birthday,scores = 0):
        self.first_name =  first_name
        self.last_name = last_name
        self.birthday = birthday
        self.scores = scores
    def score(self,winning_situation_type):
    # winner + 1 point, loser 0 point, otherwise 0.5 point for each
        if winning_situation_type == 1:
            self.scores = self.scores + 1
        elif winning_situation_type == 0:
            self.scores = self.scores + 0
        else :
            self.scores = self.scores + 0.5
        return print(self.scores)
    def print_informations_players(self):
    # a dictionary with informations of players
        informations_player = {
                               "First Name":self.first_name,
                               "Last Name":self.last_name,
                               "Birthday":self.birthday,
                               "Scores":self.scores
                               }
        print(informations_player)
    def list_of_players(self):


class Championships:
    '''
        a class that contains all the necessary informations of the championships
    '''
    round_indicator = 1
    def __init__(self,name,place,starting_date,ending_date,description,
                 player,round_indicator=1,round_total=4):
        self.name = name
        self.place = place
        self.starting_date = starting_date
        self.ending_date = ending_date
        self.round_total = round_total
        self.description = description
        self.player = player
        self.round_indicator = round_indicator
    def round(self):
    # a round indicator
        self.round_indicator = self.round_indicator + 1
        return round_indicator
    def print_informations_championship(self):
        informations_championship = {
                                     "Championship name": self.name,
                                     "Championship hold place":self.place,
                                     "Championship start date":self.starting_date,
                                     "Championship ending date":self.starting_date,
                                     "Championship total round":self.description,
                                     "Championship description":self.description,
                                     "Championship players":self.player,
                                     "Championship round ":self.round_indicator
                                  }

class Match(Championships):
    def __init__(self,round_indicator):
        super().__init__(self, round_indicator)
        self.round = round_indicator

def generate_random_opponent(List_Player):  -> Tuple[Dict[int,str]]
    '''
        for the first list of opponent,we use random function
    '''
    List_Player_Opponent = []   # a new list that contains list of opponent
    List_Temporary = []   # a temporary list
    List_Player_Opponent_round = {}
    i = 0
    random.shuffle(List_Player)
    while i < len(List_Player):
        List_Temporary = List_Player[i:i+2]
        i = i + 2
        List_Player_Opponent.append(List_Temporary)
    List_Player_Opponent_round = {1:List_Player_Opponent}
    return List_Player_Opponent_round

def generate_opponent(List_Player,List_Player_Opponent_round[]):
    '''
        generate list of opponent by the order of there points
    '''
    i = 0
    New_List_Player_Opponent = []  # a new list that contains list of opponent
    List_Temporary = []  # a temporary list
    while i < len(List_Player):
        List_Temporary.append(List_Player[0])
        List_Temporary.append(List_Player[i+1])
        #if List_Temporary in List_Player_Opponent :
        #   i = i + 1

        #ListPlayerOpponent.append(List_Temporary)
    return List_Player_Opponent_round

ListPlayer = []
List_Player_Opponent

listmatch = []