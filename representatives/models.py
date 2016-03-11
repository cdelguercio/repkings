from __future__ import unicode_literals

from django.db import models

from localflavor.us.models import USStateField


class Representative(models.Model):

    class RepresentativeType:
        CONGRESSPERSON = 0
        SENATOR = 1

    REPRESENTATIVE_TYPE = (
        (RepresentativeType.CONGRESSPERSON, 'Congressperson'),
        (RepresentativeType.SENATOR, 'Senator'),
    )

    type = models.IntegerField(choices=REPRESENTATIVE_TYPE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    state = USStateField(null=True, blank=True)
    party = models.CharField(max_length=100, null=True, blank=True)
    congressional_district_id = models.IntegerField(null=True, blank=True)
    govtrack_id = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    @staticmethod
    def get_rep_type_from_string(rep_type):

        if str(rep_type) == 'representative':
            return 0
        elif str(rep_type) == 'senator':
            return 1
        else:
            return None
