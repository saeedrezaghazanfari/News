from django.db import models

class Ticket(models.Model):
    user = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    ticket = models.TextField()

    def __str__(self):
        return self.user