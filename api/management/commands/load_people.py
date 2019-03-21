from django.core.management.base import BaseCommand, CommandError
from rest_framework.parsers import JSONParser
from api.serializers import JsonPeopleSerializer

class Command(BaseCommand):

    def handle(self, *args, **options):
        filename = 'resources/people.json'
        try:
            with open(filename, 'rb') as json_file:
                data = JSONParser().parse(json_file)
                serializer = JsonPeopleSerializer(data=data, many=True)
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(
                        self.style.SUCCESS('You have successfully loaded a list of people'))

        except OSError:
            raise CommandError('The file %s does not exist' % filename)