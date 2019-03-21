from django.contrib import admin
from .models import Company, People, Food, Tags

admin.site.register(Company)
admin.site.register(People)
admin.site.register(Food)
admin.site.register(Tags)
