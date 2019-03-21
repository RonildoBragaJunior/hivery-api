from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient
from django.contrib.auth.models import User

from api.models import Company, People
from api.serializers import PeopleSerializerAllFields, OurFriendsSerializer, FavouriteFoodsSerializer


class ViewTests(TestCase):
    fixtures = ['dumpdata.json']

    def setUp(self):
        self.client = APIClient()
        user = User.objects.create_superuser(
            username='test',
            password='test',
            email='test@test.com.au'
        )
        self.client.force_login(user)


    """
    Given a company, the API needs to return all their employees.
    Provide the appropriate solution if the company does not have any employees.
    """

    def test_company_employees_200_response(self):
        company_employees_response = self.client.get(reverse('company_employees', kwargs={'index': 1}))
        self.assertEqual(company_employees_response.status_code, status.HTTP_200_OK)

    def test_non_existing_company(self):
        index = Company.objects.all().count()
        index += 1
        response = self.client.get(reverse('company_employees', kwargs={'index': index}))
        self.assertContains(response, 'The company you choose does not exist')

    def test_company_has_no_employees(self):
        query_set = Company.objects.filter(employees__isnull=True)
        if query_set.count() != 0:
            response = self.client.get(reverse('company_employees', kwargs={'index': query_set.first().index}))
            self.assertContains(response, 'The company you choose has no employees')
        else:
            raise Exception('There is no company with no employees in order to do the test')

    def test_company_employees_response_content(self):
        people = People.objects.filter(company__isnull=False).first()
        response = self.client.get(reverse('company_employees', kwargs={'index': people.company.index}))

        data = PeopleSerializerAllFields(people.company.employees, many=True).data
        json = JSONRenderer().render(data)
        self.assertContains(response, json)

    """
    Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in
    common which have brown eyes and are still alive.
    """

    def test_our_friends_200_response(self):
        response = self.client.get(reverse('our_friends', kwargs={'people1': 1, 'people2': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_friends_in_common(self):
        people1 = People.objects.filter(friends__isnull=True).first()
        people2 = People.objects.filter(friends__isnull=False).first()

        response = self.client.get(reverse('our_friends', kwargs={'people1': people1.index, 'people2': people2.index}))
        self.assertContains(response, '%s and %s Has no friends in common' % (people2.name, people1.name))

    def test_friends_in_common(self):
        people1 = People.objects.filter(friends__isnull=False).first()
        people2 = People.objects.filter(
            friends___id__contains=people1.friends.first().index).exclude(
            index=people1.index
        ).first()

        response = self.client.get(reverse('our_friends', kwargs={'people1': people1.index, 'people2': people2.index}))

        our_friends = people1.friends.all().intersection(people2.friends.all()).filter(
            eye_color='brown', has_died=False
        )

        data = OurFriendsSerializer({
            'people1': people1,
            'people2': people2,
            'our_friends': our_friends
        }).data
        json = JSONRenderer().render(data)

        self.assertContains(response, json)

    """
    Given 1 people, provide a list of fruits and vegetables they like.
    """

    def test_favourite_foods_200_response(self):
        response = self.client.get(reverse('favourite_foods', kwargs={'index': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_favourite_foods_content(self):
        people = People.objects.first()
        json = JSONRenderer().render(FavouriteFoodsSerializer(people).data)
        response = self.client.get(reverse('favourite_foods', kwargs={'index': people.index}))
        self.assertContains(response, json)
