from django.db import models

START = "2017-05-11"


class Entry(models.Model):
    title = models.CharField(max_length=200, unique=True)
    date = models.DateTimeField()
    body = models.TextField(blank=True)  # Unlimited length.
    original_unix_time = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    # TODO Consider whether this is an antipattern.
    def year(self):
        return str(self.date.year).zfill(4)

    def month(self):
        return str(self.date.month).zfill(2)

    def day(self):
        return str(self.date.day).zfill(2)

    def fancy_text(self):
        return self.title

    def date_text(self):
        return self.date.strftime('%Y-%m-%d')


class LifeEvent(models.Model):
    body = models.TextField(blank=True)
    # The Entry to which this LiveEvent belongs. I'm not sure NULL is okay.
    event = models.ForeignKey(Entry, on_delete=models.CASCADE, null=True)


class MediaEvent(models.Model):
    STARTED = 'S'
    CONTINUED = 'C'
    FINISHED = 'F'
    MEDIA_STATUS_CHOICES = (
        (STARTED, 'Started'),
        (CONTINUED, 'Continued'),
        (FINISHED, 'Finished'),
    )
    body = models.TextField(blank=True)
    status = models.CharField(max_length=2, choices=MEDIA_STATUS_CHOICES)
    event = models.ForeignKey(Entry, on_delete=models.CASCADE, null=True)
