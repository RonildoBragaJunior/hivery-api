from django.core.management.base import BaseCommand, CommandError
from rest_framework.parsers import JSONParser
from api.models import Food

class Command(BaseCommand):

    def process(self, file_name, type_food):
        try:
            with open(file_name, 'rb') as json_file:
                data = JSONParser().parse(json_file).pop(type_food)
                for name in data:
                    food, created = Food.objects.update_or_create(name=name)
                    food.food_type = type_food
                    food.save()

        except OSError:
            raise CommandError('The file %s does not exist' % file_name)


    def handle(self, *args, **options):
        self.process('resources/fruits.json', 'F')
        self.process('resources/vegetables.json', 'V')
        self.stdout.write(
            self.style.SUCCESS('You have successfully loaded a list of food'))