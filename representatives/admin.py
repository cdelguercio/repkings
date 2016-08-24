from django.contrib import admin

from .models import Representative


class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'first_name', 'last_name', 'state', 'party', 'congressional_district_id', 'govtrack_id', 'active', )

    class Meta:
        model = Representative


admin.site.register(Representative, RepresentativeAdmin)
