from djcelery import celery
from govtrack.api import GovTrackClient

from django.core.exceptions import ObjectDoesNotExist

from .models import Representative


@celery.task
def test():
    from slothauth.mail import send_mail

    send_mail('test', 'hey chris', '<h1>hey chris</h1>', 'email@repkingsnotifications@gmail.com', 'cdelguercio@gmail.com')


@celery.task
def update_representatives():
    client = GovTrackClient()

    roles = client.role({'current': 'true', 'limit': 600})

    for role in roles['objects']:
        try:
            Representative.objects.get(govtrack_id=role['id'])
        except ObjectDoesNotExist:
            type = Representative.get_rep_type_from_string(role['role_type'])
            if type is None:
                continue
            representative = Representative(type=type, first_name=role['person']['firstname'], last_name=role['person']['lastname'], state=role['state'], party=role['party'], congressional_district_id=role['district'], govtrack_id=role['id'], active=True)
            representative.save()

    # TODO deactivate retired representatives
