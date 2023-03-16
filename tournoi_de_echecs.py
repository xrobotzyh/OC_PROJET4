class Players:

    def __init__(self,first_name,last_name,birthday,scores = 0):
        self.first_name =  first_name
        self.last_name = last_name
        self.birthday = birthday
        self.scores = scores
    def score(self,winning_situation_type):
        if winning_situation_type == 1:
            self.scores = self.scores + 1
        elif winning_situation_type == 0:
            self.scores = self.scores + 0
        else :
            self.scores = self.scores + 0.5
        return print(self.scores)
    def print_informations_players(self):
        informations_player = {
                               "First Name":self.first_name,
                               "Last Name":self.last_name,
                               "Birthday":self.birthday,
                               "Scores":self.scores
                               }
        print(informations_player)


class Championships:
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

def generateopponent(listplayer):
    pass


listplayer = []
listmatch = []