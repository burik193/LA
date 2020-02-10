import PySimpleGUI as sg
import engine

class MF:
    classes = ['Warlock', 'Mage', 'Priest', 'Rogue', 'Druid', 'DemonHunter', 'Monk', 'Hunter', 'Shaman', 'Paladin',
               'Warrior', 'DeathKnight']
    number = ''
    def __init__(self):
        layout = [[sg.Text('Создайте свой гильдейский статик!')],
                  [sg.Input('Количество рейдеров')],
                  [sg.Button('Создать список'), sg.Exit()]]

        window = sg.Window('LofD', layout)

        while True:
            event, values = window.read()
            if event is None or event == 'Exit':
                break
            elif event == 'Создать список':
                self.number = values[0]
                if self.number.isdigit():
                    self.number = int(self.number)
                else:
                    print('Неверный ввод')
                break

        window.Close()

        column = []
        guild_list = []
        for i in range(self.number):
            column.append([sg.Input(''), sg.Combo(self.classes)])

        layout = [[sg.Text('Создайте свой гильдейский статик!')],
                  [sg.Col(column)],
                  [sg.Button('Принять'), sg.Exit()]]

        window = sg.Window('LofD', layout)

        while True:
            event, values = window.read()
            if event is None or event == 'Exit':
                break
            elif event == 'Принять':
                self.guild_list = [values[i] for i in range(len(values)) if i%2 == 1]
                break

        window.Close()

    def get_guild_list(self):
        return self.guild_list

    def save_guild_list(self):
        