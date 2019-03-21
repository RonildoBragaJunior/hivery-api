from rest_framework import serializers

from api.models import Company, People, Food, Tags


"""
    Auxiliar serializers
"""
class StringListField(serializers.ListField):
    child = serializers.CharField()


"""
    Model serializers
"""
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('name', 'food_type')


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ('name',)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('index', 'company',)


class PeopleSerializerAllFields(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('__all__')


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('name', 'age', 'address', 'phone',)


class OurFriendsSerializer(serializers.Serializer):
    def to_representation(self, obj):
        return {
            'friend one': PeopleSerializer(obj['people1']).data,
            'friend two': PeopleSerializer(obj['people2']).data,
            'our common friends': PeopleSerializer(obj['our_friends'], many=True).data,
        }


class FavouriteFoodsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='name')
    vegetables = StringListField(source='favourite_vegetables_list')
    fruits = StringListField(source='favourite_fruits_list')

    class Meta:
        model = People
        fields = ('username', 'age', 'fruits', 'vegetables')


"""
    Json input serializers
"""
class JsonPeopleSerializer(serializers.Serializer):
    time_format = '%Y-%m-%dT%H:%M:%S %z'
    date_format = 'YYYY-MM-DDThh:mm[:ss[.uuuuuu]] [+HH:MM|-HH:MM|Z]'
    index = serializers.IntegerField(required=True)
    name = serializers.CharField(allow_blank=True, required=False)
    _id = serializers.CharField(allow_blank=True, required=False)
    guid = serializers.CharField(allow_blank=True, required=False)
    has_died = serializers.BooleanField(default=False, required=False)
    balance = serializers.CharField(allow_blank=True, required=False)
    picture = serializers.CharField(allow_blank=True, required=False)
    age = serializers.IntegerField(required=False)
    eyeColor = serializers.CharField(allow_blank=True, required=False)
    gender = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    phone = serializers.CharField(allow_blank=True, required=False)
    address = serializers.CharField(allow_blank=True, required=False)
    about = serializers.CharField(allow_blank=True, required=False)
    registered = serializers.DateTimeField(input_formats=[date_format, time_format], required=False)
    greeting = serializers.CharField(allow_blank=True, required=False)

    company_id = serializers.IntegerField(required=False)
    favourite_fruits = StringListField(required=False)
    favourite_vegetables = StringListField(required=False)
    tags = StringListField(required=False)
    favouriteFood = StringListField(required=False)
    friends = serializers.ListField(required=False)

    def create(self, validated_data):
        favorite_food = tags = friends = balance = eye_color = None

        if 'friends' in validated_data:
            friends = validated_data.pop('friends')
        if 'favouriteFood' in validated_data:
            favorite_food = validated_data.pop('favouriteFood')
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
        if 'company_id' in validated_data:
            company_id = validated_data.pop('company_id')
        if 'balance' in validated_data:
            balance = validated_data.pop('balance')
        if 'eyeColor' in validated_data:
            eye_color = validated_data.pop('eyeColor')

        people, created = People.objects.update_or_create(index=validated_data['index'], defaults=validated_data)
        company, created = Company.objects.get_or_create(index=company_id)
        people.company = company

        if favorite_food is not None:
            for food in favorite_food:
                food = food.strip().lower()
                food, created = Food.objects.get_or_create(name=food)
                people.favourite_food.add(food)

        if tags is not None:
            for tag in tags:
                tag = tag.strip().lower()
                tag, created = Tags.objects.get_or_create(name=tag)
                people.tags.add(tag)

        if friends is not None:
            for friend in friends:
                friend, created = People.objects.get_or_create(**friend)
                people.friends.add(friend)

        if balance is not None:
            people.balance = balance.replace('$', '').replace(',', '')

        if eye_color is not None:
            people.eye_color = eye_color.strip().lower()

        people.save()
        print('people saved %s' % str(people))

        return people
