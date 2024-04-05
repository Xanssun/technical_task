from django.contrib import admin
from .models import User, Trainer, Gym, Schedule, Record

admin.site.register(User)

admin.site.register(Trainer)

admin.site.register(Gym)

admin.site.register(Schedule)

admin.site.register(Record)
