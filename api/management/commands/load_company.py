from django.core.management.base import BaseCommand, CommandError
from rest_framework.parsers import JSONParser
from api.serializers import CompanySerializer

class Command(BaseCommand):

    def handle(self, *args, **options):
        filename = 'resources/companies.json'
        try:
            with open(filename, 'rb') as json_file:
                data = JSONParser().parse(json_file)
                serializer = CompanySerializer(data=data, many=True)
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(
                        self.style.SUCCESS('You have successfully loaded a list companies'))

        except OSError:
            raise CommandError('The file %s does not exist' % filename)