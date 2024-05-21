import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import sys
from time import sleep
from fake_useragent import UserAgent

# Filter by category:
chalCat = "Web - Serveur"

ranks = [
    ('Hacker', 5),
    ('Very very good hacker', 10),
    ('Aspiring cheater', 20),
    ('Elite cheater', 30),
    ('Legendary cheater', 50),
    ('This is too much...', 100),
]

def choose_graph_color(percentage):
    if percentage < ranks[0][1]:
        return 'lightgreen'
    elif percentage < ranks[1][1]:
        return 'green'
    elif percentage < ranks[2][1]:
        return 'orange'
    elif percentage < ranks[3][1]:
        return 'darkorange'
    elif percentage < ranks[4][1]:
        return 'red'
    else:
        return 'darkred'

class CheatPlayer:
    def __init__(self, _pseudo, _vb = True):
        self.pseudo = _pseudo
        self.vb = _vb
        self.ua = UserAgent()
        self.chals = []
        self.cheating_count = {'potential': 0, 'sure': 0}
        self.threshold = {'potential': 4, 'sure': 6}

    def fetch_challenges(self):
        try:
            headers = {'User-Agent': self.ua.random}
            url = f'https://www.root-me.org/{self.pseudo}?inc=statistiques&lang=fr'
            response = requests.get(url, headers=headers)
            if not response.ok:
                raise Exception("Failed to fetch data")
            content = response.text
            split_data = [data.split('});')[0] for data in content.split('validations.push({')[1:]]
            self.chals = [
                {
                    'name': self._get_data_value(data, "titre").split('</a>')[-2].split('>')[1],
                    'points': self._get_data_value(data, "score").replace(" ", "").replace(",\n", ""),
                    'date': self._get_data_value(data, "date"),
                }
                for data in split_data
                if chalCat in self._get_data_value(data, "titre")
            ]
            sleep(2)
        except Exception as e:
            print(f"Unable to verify this account due to error: {e}")
            return False
        return True

    def _get_data_value(self, data, key):
        return data.split(f"'{key}'")[1].split('}')[0].split("',")[0].split("',")[0].replace("'", "").split(': ')[1]

    def check_cheating(self):
        for i in range(len(self.chals) - 1):
            nextChal = self.chals[i + 1]
            time_diff = (datetime.strptime(nextChal['date'], '%Y-%m-%d %H:%M:%S') -
                         datetime.strptime(self.chals[i]['date'], '%Y-%m-%d %H:%M:%S')).total_seconds() / 60
            points = int(self.chals[i + 1]['points'])
            ratio = points / time_diff if time_diff else float('inf')

            if ratio > self.threshold['potential']:
                if ratio > self.threshold['sure']:
                    self.cheating_count['sure'] += 1
                    if self.vb:
                        print(f"\n[Cheat] - {nextChal['name']} ({nextChal['points']}pts): in (<) {int(time_diff)} min.")
                else:
                    self.cheating_count['potential'] += 1
                    if self.vb:
                        print(f"\n[Potential Cheat] - {nextChal['name']} ({nextChal['points']}pts): in (<) {int(time_diff)} min.")

        return True

    def print_results(self):
        if not self.chals or not self.check_cheating():
            print("No challenges to analyze or error in processing.")
            return 0
        
        ratio_sure = self.cheating_count['sure'] / len(self.chals) * 100
        ratio_potential = self.cheating_count['potential'] / len(self.chals) * 100

        for rank, threshold in ranks:
            if ratio_sure <= threshold:
                print(f"####### Rank: {rank} #######")
                break

        print(f"####### {self.cheating_count['sure']} cheats detected | ~ {self.cheating_count['potential']} potential cheats detected #######")
        print(f"####### {int(ratio_sure)}% cheated | ~ {int(ratio_potential)}% potentially cheated #######")

        return int(ratio_sure)

def main():
    pseudos = sys.argv[1:]

    if len(pseudos) <= 0:
        pseudos = input("Rootme pseudo (url): ").replace(" ", "").split(',')

    if len(pseudos) == 1:
        print(f"\n_____________________ {pseudos[0]} _____________________")
        player = CheatPlayer(pseudos[0])
        if player.fetch_challenges():
            player.print_results()
    else:
        dpseudo = []
        dpourct = []

        for pseudo in pseudos:
            print(f"\n_____________________ {pseudo} _____________________")
            player = CheatPlayer(pseudo, False)
            if player.fetch_challenges():
                dpseudo.append(pseudo)
                dpourct.append(player.print_results())
            else:
                print(f"Error for scrap {pseudo}...")

        showOnlyCheaters = input("\n\n>> Show only cheaters ? (Y,n): ")

        if showOnlyCheaters.lower() == "y":
            indicesToTemove = [i for i, value in enumerate(dpourct) if value <= 10]

            for index in reversed(indicesToTemove):
                dpourct.pop(index)
                dpseudo.pop(index)


        # DISPLAY GRAPHS:
        if len(dpourct) > 0:
            plt.figure(figsize=(10, 5))

            combined = zip(dpourct, dpseudo)
            sorted_combined = sorted(combined, reverse=True, key=lambda x: x[0])
            dpourct_sorted, dpseudo_sorted = zip(*sorted_combined)

            bars = plt.bar(dpseudo_sorted, dpourct_sorted, color=[choose_graph_color(percentage) for percentage in dpourct_sorted])

            plt.title('Percentage of Cheating by Nickname')
            plt.xlabel('Pseudo')
            plt.ylabel('Cheat Percentage (%)')

            for bar, percentage in zip(bars, dpourct_sorted):
                y_val = bar.get_height() / 2
                plt.text(bar.get_x() + bar.get_width() / 2, y_val, f'{percentage}%', ha='center', va='center')

            plt.show()
        else:
            print("\n\n#### NO CHEATERS ####")

if __name__ == "__main__":
    main()
