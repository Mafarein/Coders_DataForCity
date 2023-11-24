# wykorzystane jednorazowo z użyciem manage.py shell

from django.contrib.auth.models import Group

Group(name="RegularUsers").save()
Group(name="SportFacilityOwners").save()
Group(name="Schools").save()
