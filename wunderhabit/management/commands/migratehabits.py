from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from wunderlist.models import Connection


class Command(BaseCommand):
    help = 'Migrates the habits from Habitica API v2 to v3'

    def handle(self, *args, **options):
        users = User.objects.all()
        active_connections = Connection.objects.filter(is_active=True).count()
        modified_connections = 0

        for user in users:
            # Get connections of the user
            connections = Connection.objects.filter(owner=user)

            if connections.count() == 0:
                continue

            # Get habits of the user
            try:
                habits = user.habitica.get_api().get_habits()
            except Exception as e:
                print('No habits for user ' + str(user) + ': ' + str(e))
                continue

            # Iterate over all connections
            for connection in connections:
                for habit in habits:
                    if '_legacyId' not in habit:
                        continue
                    if connection.habit_id == str(habit['_legacyId']):
                        habit_id = habit['id']
                        habit_title = habit['text']
                        break

                if habit_id is None or habit_title is None:
                    # Disable connection
                    print('Disabling connection: ' + str(connection.id))
                    connection.deactivate()

                print(str(
                    connection.id) + ' ' + connection.list_title + ' -> ' + connection.habit_id + ': ' + habit_id + ' ' + habit_title)
                connection.habit_id = habit_id
                connection.habit_title = habit_title
                connection.save()
                modified_connections += 1

        print('Active connections before and after:', active_connections, Connection.objects.filter(is_active=True).count())
        print('Modified connections: ', modified_connections)
