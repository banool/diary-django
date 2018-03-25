from django.contrib import admin


from .models import Entry, LifeEvent, MediaEvent

admin.site.register(Entry)
admin.site.register(LifeEvent)
admin.site.register(MediaEvent)
