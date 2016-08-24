from djcelery import celery
from govtrack.api import GovTrackClient

from django.core.exceptions import ObjectDoesNotExist

from representatives.models import Representative

from .models import Bill, Vote


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
            votes = []

            if db_bill.current_status == Bill.BillStatus.PASSED_HOUSE or \
                    db_bill.current_status == Bill.BillStatus.FAILED_HOUSE or \
                    db_bill.current_status == Bill.BillStatus.PASSED_SENATE or \
                    db_bill.current_status == Bill.BillStatus.FAILED_SENATE:

                # set votes for all congresspeople and senators
                votes = client.vote({'related_bill': bill['id'], 'limit': 600})

                #print votes

                for vote in votes['objects']:
                    #print vote
                    vote_voters = client.vote_voter({'vote': vote['id'], 'limit': 600})

                    for vote_voter in vote_voters['objects']:
                        #print vote_voter

                        try:
                            representative = Representative.objects.get(govtrack_id=vote_voter['person_role']['id'])

                            try:
                                Vote.objects.get(bill=db_bill, representative=representative)

                            except ObjectDoesNotExist:

                                vote_option = vote_voter['option']['key']

                                if vote_option == '+':
                                    vote_value = Vote.VoteOption.AYE
                                elif vote_option == '-':
                                    vote_value = Vote.VoteOption.NO
                                elif vote_option == '0':
                                    vote_value = Vote.VoteOption.NOT_VOTING
                                elif vote_option == 'P':
                                    vote_value = Vote.VoteOption.PRESENT
                                else:
                                    raise Exception('Invalid vote_voters Option Key value')

                                new_vote = Vote(bill=db_bill, vote=vote_value, representative=representative, vote_date=vote['created'])
                                new_vote.save()

                        except ObjectDoesNotExist:
                            print "ERROR: Representative doesn't exist:"
                            print vote_voter


###
# notify users
#
#  Uses date_created fields for Bills to show new bills and date_created
#  for votes to show new votes (created in the last 24 hours)
###
@celery.task
def notify_users():
    pass
