from __future__ import unicode_literals

from django.db import models

from representatives.models import Representative


class Bill(models.Model):

    class BillStatus:
        NONE = 0
        INTRODUCED = 1
        REPORTED = 2
        PASSED_HOUSE = 3
        FAILED_HOUSE = 4
        PASSED_SENATE = 5
        FAILED_SENATE = 6

    BILL_STATUS = (
        (BillStatus.NONE, 'None'),
        (BillStatus.INTRODUCED, 'Introduced'),
        (BillStatus.REPORTED, 'Reported'),
        (BillStatus.PASSED_HOUSE, 'Passed House'),
        (BillStatus.FAILED_HOUSE, 'Failed House'),
        (BillStatus.PASSED_SENATE, 'Passed Senate'),
        (BillStatus.FAILED_SENATE, 'Failed Senate'),
    )

    current_status = models.PositiveIntegerField(default=BillStatus.NONE, choices=BILL_STATUS)
    bill_type = models.CharField(max_length=100)
    introduced_date = models.DateTimeField()
    current_status_date = models.DateTimeField()
    govtrack_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    title_without_number = models.CharField(max_length=1000, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)  # TODO mixin

    @staticmethod
    def get_current_status_from_string(current_status):

        if str(current_status) == 'introduced':
            return 1
        if str(current_status) == 'reported':
            return 2
        elif str(current_status) == 'pass_over_house':
            return 3
        elif str(current_status) == 'pass_over_senate':
            return 4
        elif str(current_status) == 'fail_originating_house':
            return 5
        elif str(current_status) == 'fail_originating_senate':
            return 6
        else:
            return 0


class Vote(models.Model):

    class VoteOption:
        NOT_VOTING = 0
        PRESENT = 1
        AYE = 2
        NO = 3

    VOTE_OPTION = (
        (VoteOption.NOT_VOTING, 'Not Voting'),
        (VoteOption.PRESENT, 'Present'),
        (VoteOption.AYE, 'Aye'),
        (VoteOption.NO, 'No'),
    )

    representative = models.ForeignKey(Representative)
    bill = models.ForeignKey(Bill)
    vote = models.IntegerField(default=VoteOption.NOT_VOTING, choices=VOTE_OPTION)
    vote_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)  # TODO mixin
