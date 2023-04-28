from typing import Dict, Any
from jinja2 import Template


class View:

    def __init__(self, header, footer):
        self.header = header
        self.header_main = "\n*What do you want to do ?"
        self.header_add_tournament = "*Please complete the information below"
        self.footer = footer

    def display_main_menu(self, choices: Dict[str, str]):

        # a block to show add a new tournament,after the input return to the main menu
        print(self.header)
        choice = None
        self.display_dicts(choices)
        while choice not in choices:
            choice = input(self.footer)
        return choice

    def display_menu(self, choices: Dict[str, str]):
        print(self.header_main)
        choice = None
        self.display_dicts(choices)
        while choice not in choices:
            choice = input(self.footer)
        return choice

    def get_user_inputs(self, input_fields: Dict[str, Any]) -> Dict[str, str]:
        # Note for improvements: user input validation
        user_inputs = {}
        for key, value in input_fields.items():
            value = input(f'Input for {value}\n')
            user_inputs[key] = value
        return user_inputs

    def get_user_input(self, prompt: str) -> str:
        # Note for improvements: user input validation
        return input(f'{prompt}\n')

    def display_message(self, message):
        print(message)

    def display_dicts(self, dicts):
        # a function that will show the dictionary line by line

        for key, value in dicts.items():
            print(f'{key}: {value}')

    def display_report_template(self):
        template = Template('''
        <html>
        <head>
            <title>{{ report_title }}</title>
        </head>
        <body>
            <h1>{{ report_title }}</h1>
            <table>
                <tr>
                    {% for column in columns %}
                    <th>{{ column }}</th>
                    {% endfor %}
                </tr>
                {% for item in report_data %}
                <tr>
                    {% for column in columns %}
                    <td>{{ item[column] }}</td>
                    {% endfor %}
                </tr>
                {% endfor %}
            </table>
        </body>
        </html>
        ''')
        return template
