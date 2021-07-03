from django.db import models
from .sentiment_analysis_code import sentiment_analysis_code

# Create your models here.
class Tweet(models.Model):
	content = models.TextField()
	sentiment = models.CharField(max_length=255)
	waktuInput = models.DateTimeField(auto_now_add = True)



	def __str__(self):
		return "{}. {}".format(self.id, self.content)