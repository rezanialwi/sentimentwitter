from django.contrib import admin

# Register your models here.
from .models import Tweet

class TweetAdmin(admin.ModelAdmin):
	readonly_fields = [
						'waktuInput',

	]

admin.site.register(Tweet,TweetAdmin)

