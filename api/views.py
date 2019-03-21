from django.core.exceptions import ObjectDoesNotExist
from rest_framework import views
from rest_framework.response import Response

from api.models import Company, People
from api.serializers import OurFriendsSerializer, FavouriteFoodsSerializer, PeopleSerializerAllFields


class CompanyEmployeesView(views.APIView):
    def get(self, request, index):
        try:
            company = Company.objects.get(index=index)
        except ObjectDoesNotExist:
            return Response({'The company you choose does not exist'})

        employees = company.employees.all()

        if employees.count() == 0:
            return Response({'The company you choose has no employees'})

        return Response(PeopleSerializerAllFields(employees, many=True).data)


class OurFriendsView(views.APIView):
    def get(self, request, people1, people2):
        people_list = People.objects.filter(index__in=(people1, people2))

        if people_list.count() == 2:
            my_friends = people_list[0].friends.all()
            your_friends = people_list[1].friends.all()

            our_friends = my_friends.intersection(your_friends).filter(
                eye_color='brown', has_died=False
            )

            if our_friends.count() != 0:
                serializer = OurFriendsSerializer({
                    'people1': people_list[0],
                    'people2': people_list[1],
                    'our_friends': our_friends
                })
                return Response(serializer.data)
            else:
                return Response({'%s and %s Has no friends in common' % (people_list[0].name, people_list[1].name)})
        else:
            return Response({'Please choose people who exist'})


class FavouriteFoodsView(views.APIView):
    def get(self, request, index):
        try:
            people = People.objects.get(index=index)
            return Response(FavouriteFoodsSerializer(people).data)

        except ObjectDoesNotExist:
            return Response({'Please choose someone from the people list'})
