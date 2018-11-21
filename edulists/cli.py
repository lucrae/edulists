import click
import secrets
import csv

from edulists import db
from edulists.models import Subject

def register(app):

    @app.cli.group()
    def security():
        '''Access security and config information'''
        pass

    @security.command('config')
    def display_config():
        '''Display configuration variables'''

        details = app.config
        print(f'Config variables for "{app.name}":')
        for detail in details:
            print(f'\t {detail}: {details[detail]}')

    @security.command('genhex')
    @click.argument('length')
    def generate_hex_token(length):
        '''Randomly generate a hex token'''

        token = secrets.token_hex(int(length) // 2)
        print(token)

    @app.cli.group()
    def data():
        '''Interact with data files'''
        pass

    @data.command('subjects')
    def subjects():
        '''Parse subjects and insert into the database'''

        subject_lists = {
            'GEN': [],
            'VCE': [],
            'HSC': [],
            'QCE': [],
        }

        # read in subjects from csv file
        with open('data/subjects.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in list(reader)[1:]:
                subject_lists[row[1]].append(row)

        # sort each lists
        for c in subject_lists:
            subject_lists[c] = sorted(subject_lists[c], key=lambda x:x[0].lower())

            # insert into database
            for subject in subject_lists[c]:
                s = Subject(subject[0], subject[1])
                db.session.add(s)
                db.session.commit()

                print(f'INSERT SUCCESSFUL: {s}')