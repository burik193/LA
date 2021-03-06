import client
import PySimpleGUI as sg
import pandas as pd
import webbrowser
import mainframe


zone_info = {}
raid_info = {}
zone_list = []
boss_list = []


class Engine:
    boss_name = ''
    def __init__(self):
        self.key = '866b2f014c35f4ce418d12ecbb713388'#create zone names
        self.connection = client.WarcraftLogsClient(api_key=self.key)
        self.Zones = self.connection.zones()

    def get_zone(self):
        column = []
        saved_key = []
        for zone in self.Zones:
            zone_info[zone['name']] = zone['id']
            zone_list.append(zone['name'])
            column.append([sg.CB(zone['name'])])

        layout = [[sg.Text('Choose a zone')],
                  [sg.Col(column)],
                  [sg.Button('Select'), sg.Exit()]]

        window = sg.Window('All zones', layout)

        while True:
            event, values = window.Read()
            if event is None or event == 'Exit':
                break
            elif event == 'Select':
                for key in values:
                    if values[key]:
                        saved_key = key
            break

        window.Close()
        print(zone_list[saved_key])
        return zone_list[saved_key]

    def get_boss(self, raid_name):
        column = []
        saved_key = []
        id_zone = zone_info[raid_name]
        raid = self.Zones[id_zone - 3]['encounters']
        for encounter in raid:
            raid_info[encounter['name']] = encounter['id']
            column.append([sg.CB(encounter['name'])])
            boss_list.append(encounter['name'])

        layout = [[sg.Text('Choose a boss')],
                  [sg.Col(column)],
                  [sg.Button('Search online'), sg.Button('Search offline'), sg.Exit()]]

        window = sg.Window('All bosses', layout)
        search = True

        while True:
            event, values = window.Read()
            if event is None or event == 'Exit':
                break
            elif event == 'Search online':
                for key in values:
                    if values[key]:
                        saved_key = key
                search = True
            elif event == 'Search offline':
                for key in values:
                    if values[key]:
                        saved_key = key
                search = False
            break
        window.Close()
        print(boss_list[saved_key])
        self.boss_name = boss_list[saved_key]
        return search

        #need new function
    def get_setups(self, guild_list):
        # id_Nyalotha = zone_info[raid_name]                  #for ex. Ny\'alotha
        # raid = self.Zones[id_Nyalotha-3]['encounters']
        # for encounter in raid:
        #     raid_info[encounter['name']] = encounter['id']

        rankings = self.connection.rankings_encounter(raid_info[self.boss_name])         #'Wrathion'
        length = len(rankings)
        print(length)
        reportID = []
        fightID = []
        counter = 0
        list_of_lists = []
        column = []
        saved_key = []
        path = []


        layout = [[sg.Text('Ищем сетапы')],
                  [sg.ProgressBar(length, orientation='h', size=(20, 20), key='progressbar')],
                  [sg.Cancel()]]

        # create the window`
        window = sg.Window('Custom Progress Meter', layout)
        progress_bar = window['progressbar']
        # loop that would normally do something useful
        for j in rankings:
            # check to see if the cancel button was clicked and exit loop if clicked
            event, values = window.read(timeout=10)
            if event == 'Cancel' or event is None:
                break
            # update bar with loop value +1 so that bar eventually reaches the maximum
            # Comberdale_guildName = rankings[0]['guildName']
            # Comberdale_serverName = rankings[0]['serverName']
            # Comberdale_serverRegion = rankings[0]['regionName']
            reportID.append(j['reportID'])
            fightID.append(j['fightID'])
            #region_name = j['regionName']
            report_fights = self.connection.report_fights(reportID[counter])
            #report_events = self.connection.report_events(reportID=reportID[counter])
            list_classes = []

            for player in report_fights['friendlies']:
                for player_id in player['fights']:
                    if fightID[counter] == player_id['id']:
                        list_classes.append(player['type'])

            diff = difference(list_classes, guild_list)  #difference of the classes
            percent = len(diff)/20
            list_of_lists.append(list_classes)           #for saving
            if percent <= 0.2:
                column.append([sg.CB(str(percent)+str('warcraftlogs.com/reports/{}'.format(reportID[counter])))])
                path.append('warcraftlogs.com/reports/{}'.format(reportID[counter]))
            list_of_lists.append(path)
            counter = counter + 1
            print(counter)
            progress_bar.UpdateBar(counter)
            if counter == length:
                break
        # done with loop... need to destroy the window as it's still open
        window.close()

        layout = [[sg.Text('Choose a setup')],
                  [sg.Col(column, scrollable=True, size=(600, 800))],
                  [sg.Button('Select'), sg.Exit()]]

        window = sg.Window('First 100 fights', layout)

        while True:
            event, values = window.Read()
            if event is None or event == 'Exit':
                break
            elif event == 'Select':
                for key in values:
                    if values[key]:
                        saved_key = key
                        webbrowser.open(path[saved_key])
            break
        window.Close()
        print(list_of_lists[saved_key])
        df = pd.DataFrame(list_of_lists)
        name = '{}.csv'.format(self.boss_name)
        df.to_csv(name, index=False, header=False)
        return list_of_lists[saved_key]

    def get_setups_offline(self, guild_list):
        file = sg.popup_get_file('Укажите сохраненные сетапы на определенного босса')
        df = pd.read_csv(file)
        rows = df[::-1]
        column = []
        path = []
        for i in rows:
            diff = difference(i, guild_list)  # difference of the classes
            percent = len(diff) / 20
            if percent <= 0.2:
                column.append([sg.CB(str(percent))])
                path.append(rows[len(rows)])

    def clean_string(self, string):
        dict = [' ', ',', '.', '/', '\\', '|', ';', ':', '[', ']', '+', '*', '@', '!', '#', '$', '%', '&', '(', ')', '}',
                '{', '?', '\'', '~', '´', '\"', '`', '<', '>', '`', '^', '°', '\n', '\t', '\s']
        string_list = string.split()
        new_string = ''
        for word in string_list:
            word = word.strip()
            for i in dict:
                word = word.replace(i, '')
            word = word.strip().lower()
            new_string = new_string + '' + word
        return new_string


def difference(minuend, subtrahend):
    for i in subtrahend:
        if i in minuend:
            subtrahend.remove(i)
    return subtrahend
# fight_recap = connection.report_guild_fights(Comberdale_guildName, Comberdale_serverName, Comberdale_serverRegion)
# print(fight_recap)



# dicts = {}
# keys = range(4)
# values = ["Hi", "I", "am", "John"]
# for i in keys:
#     for x in values:
#         dicts[i] = x