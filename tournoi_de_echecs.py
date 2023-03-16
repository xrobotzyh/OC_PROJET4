class Players:
    scores = 0
    def __init__(self,first_name,last_name,birthday):
        self.first_name =  first_name
        self.last_name = last_name
        self.birthday = birthday
    def score(self,winning_situation_type):
        if winning_situation_type == 1：
            scores = scores + 1
        elif winning_situation_type == 0:
            scores = scores + 0
        else :
            scores = scores + 0.5
        return scores
    def print_informations_players(self):
        return self.first_name,self.last_name,self.birthday

class Championships:
    round_indicator = 1
    def __init__(self,name,place,starting_date,ending_date,round_total=4,
                 description):
        self.name = name
        self.place = place
        self.starting_date = starting_date
        self.ending_date = ending_date
        self.round_total = round_total
        self.description = description
    def round(self):
        round_indicator = round_indicator + 1
        return round_indicator

class Match(Championships)：
    def __init__(self,round_indicator)
        super()__init__(self, round_indicator)
        self.round = round_indicator

    def
