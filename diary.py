from collections import OrderedDict
import datetime

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    #create database and the table if they don't exist
    db.connect()
    db.create_tables([Entry], safe=True)


def view_menu():
    '''View diary's menu.'''
    choice = None
    while choice != 'q':
        print("Enter q to quit")
        for k,v in menu.items():
            print('{}){}'.format(k,v.__doc__))
        choice = input('Action: ').lower().strip()
        if choice in menu:
            menu[choice]()


def add_entry():
    """Add an entry."""
    entry = ""
    print("Log you idea, print 'done' to finish.")
    while True:
        data = input('> ')
        if data.lower() != 'done':
            entry += data + "\n"
        else:
            break
    # data = sys.stdin.read().strip()

    if entry:
        if input('Save entry? [Y]/n ').lower() != 'n':
            Entry.create(content=entry)
            print("Saved!")
        else:
            print("Your entry wasn't save")


def view_entries(search_query=None):
    '''View an entry.'''
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))
    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print(entry.content)
        print('n) next entry')
        print('d) delete entry')
        print('q) back to menu')

        next_action = input('Action: [n/d/q]').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def delete_entry(entry):
    '''Delete an entry'''
    if input('Are you sure? [y/n]').lower() == 'y':
        entry.delete_instance()


def search_entries():
    '''Search for an entry'''
    view_entries(input('Search query: '))


menu = OrderedDict([
    ('a', add_entry),
    ('d', delete_entry),
    ('s', search_entries),
    ('v', view_entries)
])


if __name__ == '__main__':
    initialize()
    view_menu()