from __future__ import unicode_literals

from localflavor.us.models import USZipCodeField

from slothauth.models import SlothAuthBaseUser


class Account(SlothAuthBaseUser):
    zip_code = USZipCodeField()
