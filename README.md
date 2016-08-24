# RepKings

### Testing Procedure

```
python manage.py shell

from representatives.tasks import *
update_representatives()

from bills.tasks import *
update_bills()
```