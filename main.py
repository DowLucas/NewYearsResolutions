import argparse
import json
from datetime import datetime
import re

class Resolutions:
    dir = 'JSON'
    name = 'main.json'
    full_dir = dir+'/'+name
    def __init__(self):
        pass

    def reset(self):
        confirm = input('Please Confirm file reset by typing "confirm": ')
        if confirm == 'confirm':
            with open(self.full_dir, 'w') as j:
                structure = {
                    'Entries': [

                    ]
                }
                json.dump(structure, j, indent=4)
        print('Reset complete...')
        quit()


    @staticmethod
    def getDate():
        now = datetime.now()
        return now.strftime("%d-%m-%Y")

    def getEntry(self, date):
        with open(self.full_dir) as j:
            data = json.load(j)
            entries = data['Entries']
            return entries[date]


    def addEntry(self):
        now = datetime.now()
        Date = now.strftime("%d-%m-%Y")

        with open(self.full_dir) as j:
            data = json.load(j)
            assert Date not in data["Entries"].keys(), 'Entry already exists!'

            # Add Inputs here
            structure = {
                'Push-ups': input('Number of push-ups: '),
                'Max push-ups': input('Max push-ups: '),
                'Sit-ups': input('Number of sit-ups: '),
                'Max Sit-ups': input('Max Sit-ups: '),
                'Went to Gym': input('Went to gym?: '),
                'Other Activity': input('Other Activity?: ')
            }

            data['Entries'][Date] = structure
            j.close()

        with open(self.full_dir, 'w') as j:
            json.dump(data, j, indent=4)

    def addDateEntry(self):
        date = input('Please input date you wish to enter (format: dd-mm-yyyy) type "t" for today: ')
        if date == "t":
            self.addEntry()
            return

        with open(self.full_dir) as j:
            data = json.load(j)
            assert date not in data["Entries"].keys(), 'Entry already exists!'

            # Add Inputs here
            structure = {
                'Push-ups': input('Number of push-ups: '),
                'Max push-ups': input('Max push-ups: '),
                'Sit-ups': input('Number of sit-ups: '),
                'Max Sit-ups': input('Max Sit-ups: '),
                'Went to Gym': input('Went to gym?: '),
                'Other Activity': input('Other Activity?: ')
            }

            data['Entries'][date] = structure
            j.close()

        with open(self.full_dir, 'w') as j:
            json.dump(data, j, indent=4)




    def updateEntry(self):
        date = self.getDate()
        print(f'----- Update Entry -----\nCurrent Date: {date}')
        input_date = input('Please input date you wish to enter (format: dd-mm-yyyy) type "t" for today: ')

        if input_date == 't':
            entry = self.getEntry(date)
        else:
            try:
                datetime.strptime(date, "%d-%m-%Y")
            except Exception as E:
                print(E)
            date = input_date
            entry = self.getEntry(date)

        print('\nUpdate values of entry. Insert desired value or press enter to be unchanged.\n')

        for key in entry.keys():
            inp = input(key+f' (current: {entry[key]}): ')
            if inp == '':
                inp = entry[key]
            entry[key] = inp


        with open(self.full_dir) as j:
            data = json.load(j)
            data['Entries'][date] = entry
            with open(self.full_dir, 'w') as j:
                json.dump(data, j, indent=4)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add/Update Entries for each day')
    parser.add_argument('--add', const='add', help='Add entry', action='store_const')
    parser.add_argument('--dateadd', const='add', help="add entry based on date", action='store_const')
    parser.add_argument('--update', const='update', help='Update entry', action='store_const')
    parser.add_argument('--reset', const='reset', help='Update entry', action='store_const')

    args = parser.parse_args()

    res = Resolutions()

    if args.add:
        res.addEntry()
    elif args.dateadd:
        res.addDateEntry()
    elif args.update:
        res.updateEntry()
    elif args.reset:
        res.reset()



