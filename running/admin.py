from django.contrib import admin
from .models import Country, Province, Area, City


# Register your models here.
@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    search_fields = ('chn_name', 'eng_name')


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ('chn_name', 'eng_name')


class CityAdmin(admin.ModelAdmin):
    # 定义自动完成的字段
    autocomplete_fields = ['provinceid', 'countryid']
    list_display = ('cityid', 'countryid', 'areaid', 'provinceid', 'chn_name', 'eng_name')


admin.site.register(City, CityAdmin)
admin.site.register(Area)
