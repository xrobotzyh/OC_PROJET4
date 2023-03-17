from typing import List


class ConsoleView:
    def __init__(self):
        pass

    def show_choices(self, title: str, choices: List[str]) -> int:
        print(title + '\n*****\n')
        for index, choice in enumerate(choices):
            print(f'{index + 1}. {choice}')

        choice = input('Votre choix > ')
        return int(choice)
