from django.contrib import admin

from .models import Bill, Vote


class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'current_status', 'bill_type', 'introduced_date', 'current_status_date', 'govtrack_id', 'date_created', )

    class Meta:
        model = Bill


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'representative', 'bill', 'vote', 'vote_date', 'date_created', )

    class Meta:
        model = Vote


admin.site.register(Bill, BillAdmin)
admin.site.register(Vote, VoteAdmin)
