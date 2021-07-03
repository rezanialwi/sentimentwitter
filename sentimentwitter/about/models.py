from django.db import models

# Create your models here.
class Post(models.Model):
	sentiment = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	content = models.TextField()

	def __str__(self):
		return "{}. {}".format(self.id, self.sentiment)