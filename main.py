from tournoi_de_echecs import Players,Championships


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    playA = Players("三","张",19790506)
    playA.score(1)
    playA.print_informations_players()
    playA.score(1)
    playA.print_informations_players()
    playA.score(1)
    playA.print_informations_players()
    playB = Players("lily","ding",19800415)
    championshipA = ("big game","lyon","1502","1503","have fun",[playA,playB])
    championshipA.print_informations_championships()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
