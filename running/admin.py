from django.contrib import admin
from .models import Country, Province, Area, City

# Register your models here.
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(Area)
admin.site.register(City)
