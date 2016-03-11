from djcelery import celery
from govtrack.api import GovTrackClient

from django.core.exceptions import ObjectDoesNotExist

from .models import Bill


@celery.task
def test():
    from slothauth.mail import send_mail

    send_mail('test', 'hey chris', '<h1>hey chris</h1>', 'email@repkingsnotifications@gmail.com', 'cdelguercio@gmail.com')


@celery.task
def update_bills():
    client = GovTrackClient()

    bills = client.bill({'bill_type__in': 'house_bill|senate_bill', 'order_by': '-current_status_date', 'current_status__in': 'reported|pass_over_house|pass_over_senate|fail_originating_house|fail_originating_senate', 'limit': 600})

    for bill in bills['objects']:
        changed = False
        try:
            db_bill = Bill.objects.get(govtrack_id=bill['id'])

            if db_bill.current_status != Bill.get_current_status_from_string(bill['current_status']):
                db_bill.current_status = Bill.get_current_status_from_string(bill['current_status'])
                db_bill.save()
                changed = True
        except ObjectDoesNotExist:
            changed = True
            current_status = Bill.get_current_status_from_string(bill['current_status'])
            if current_status is None:
                continue
            db_bill = Bill(current_status=current_status, bill_type=bill['bill_type'], introduced_date=bill['introduced_date'], current_status_date=bill['current_status_date'], govtrack_id=bill['id'])
            db_bill.save()

        if changed:
            if db_bill.current_status == Bill.BillStatus.PASSED_HOUSE or db_bill.current_status == Bill.BillStatus.FAILED_HOUSE:
                pass
                # TODO set votes for all congresspeople
            elif db_bill.current_status == Bill.BillStatus.PASSED_SENATE or db_bill.current_status == Bill.BillStatus.FAILED_SENATE:
                pass
                # TODO set votes for all senators


###
# notify users
#
#  Uses date_created fields for Bills to show new bills and date_created
#  for votes to show new votes (created in the last 24 hours)
###
@celery.task
def notify_users():
    pass
