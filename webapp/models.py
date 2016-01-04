from django.db import models

class Course(models.Model):
    prereq = models.ManyToManyField("self", symmetrical=False)
    id = models.CharField(max_length=15, primary_key=True)
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.id + ' - ' + self.title
