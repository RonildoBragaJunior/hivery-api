from django.db import models
from django.core.validators import RegexValidator


GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'),)
TYPE_FOOD = (('F', 'Fruit'), ('V', 'Vegetable'), ('U', 'Unknown'))
PHONE_REGEX = RegexValidator(regex=r'^\+?1?\d{9,15}$',message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")


class Food(models.Model):
    name = models.CharField(max_length=20, unique=True)
    food_type = models.CharField(max_length=1, choices=TYPE_FOOD, default='U')

    def __str__(self):
        return "%s - %s" % (self.name, self.food_type)


class Tags(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return "%s" % self.name


class Company(models.Model):
    index = models.IntegerField(primary_key=True, unique=True)
    company = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return "%s" % self.company


class People(models.Model):
    # Primary keys and unique keys
    index = models.IntegerField(primary_key=True)
    _id = models.CharField(max_length=64, unique=True, blank=True, null=True)
    guid = models.CharField(max_length=64, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    # Foreign keys and other relationships
    favourite_food = models.ManyToManyField(Food)
    tags = models.ManyToManyField(Tags)
    company = models.ForeignKey(Company, related_name="employees", blank=True, null=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField(to='self', blank=True, symmetrical=False)
    # General fields
    name = models.CharField(max_length=64, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    has_died = models.BooleanField(blank=True, null=True)
    balance = models.DecimalField(max_digits=64, decimal_places=2, blank=True, null=True)
    picture = models.URLField(blank=True, null=True)
    eye_color = models.CharField(max_length=10, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(validators=[PHONE_REGEX],max_length=17, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    registered = models.DateField(blank=True, null=True)
    greeting = models.TextField(blank=True, null=True)

    @property
    def favourite_fruits(self):
        return self.favourite_food.all().filter(food_type='F')

    @property
    def favourite_vegetables(self):
        return self.favourite_food.all().filter(food_type='V')

    @property
    def unknown_favourite_food(self):
        return self.favourite_food.all().filter(food_type='U')

    @property
    def favourite_fruits_list(self):
        return self.favourite_fruits.values_list('name', flat=True)

    @property
    def favourite_vegetables_list(self):
        return self.favourite_vegetables.values_list('name', flat=True)

    @property
    def unknown_favourite_food_list(self):
        return self.unknown_favourite_food.values_list('name', flat=True)

    def __str__(self):
        return "%s - %s - %s - %s" % (self.index, self._id, self.name, self.email)
