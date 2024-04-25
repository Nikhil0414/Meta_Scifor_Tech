# userModule/admin.py

from django.contrib import admin
from .models import Usertbl,Orderstbl,Payment

admin.site.register(Usertbl)
admin.site.register(Orderstbl)
admin.site.register(Payment)