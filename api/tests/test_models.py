from django.test import TestCase

from api.models import Food, Tags, Company, People
from api.tests.factory import CompanyFactory, TagsFactory, FoodFactory, PeopleFactory


class ModelTestCase(TestCase):

    def setUp(self):
        pass

    def test_food_creation(self):
        food = FoodFactory()
        self.assertTrue(isinstance(food, Food))
        self.assertEqual(food.__str__(), str(food))

    def test_tags_creation(self):
        tags = TagsFactory()
        self.assertTrue(isinstance(tags, Tags))
        self.assertEqual(tags.__str__(), str(tags))

    def test_company_creation(self):
        obj = CompanyFactory()
        self.assertTrue(isinstance(obj, Company))
        self.assertEqual(obj.__str__(), str(obj))

    def test_people_creation(self):
        obj = PeopleFactory()
        self.assertTrue(isinstance(obj, People))
        self.assertEqual(obj.__str__(), str(obj))
