import factory
from api.models import Company, People, Food, Tags

class FoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Food
        django_get_or_create = ('name',)

    name = factory.Faker('name')

class TagsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tags
        django_get_or_create = ('name',)

    name = factory.Faker('name')

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
        django_get_or_create = ('company',)

    company = factory.Faker('name')

class PeopleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = People
        django_get_or_create = ('name',)

    name = factory.Faker('name')