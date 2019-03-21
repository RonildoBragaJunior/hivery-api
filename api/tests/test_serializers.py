from django.test import TestCase

from api.models import Food, Tags, Company
from api.serializers import FoodSerializer, TagsSerializer, CompanySerializer, PeopleSerializer


class SerializerTestCase(TestCase):

    def setUp(self):
        pass

    def test_food_serializer(self):
        data = {
            'name': 'Mark Neal',
            'food_type': 'U'
        }
        serializer = FoodSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIsInstance(serializer.save(), Food)

    def test_tags_serializer(self):
        data = {
            'name': 'Internet',
        }
        serializer = TagsSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIsInstance(serializer.save(), Tags)

    def test_company_serializer(self):
        data = {
            'index': 1,
            'company': 'Troy Powell'
        }
        serializer = CompanySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertIsInstance(serializer.save(), Company)