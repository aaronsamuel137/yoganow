from django.db import models

class Count(models.Model):
    num_vists = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.num_vists)

class Post(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title