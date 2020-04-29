from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):

	PRIVACY_TYPE = (
			("public" , "public") ,
			("private" , "private")
		)

	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	privacy = models.CharField(default='public', choices = PRIVACY_TYPE, max_length = 10)

	

	def __str__(self):
		return self.title



	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})



class PostComments(models.Model):
	content = models.TextField()
	date_posted = models.DateTimeField(default= timezone.now)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	authors = models.ForeignKey(User, on_delete=models.CASCADE, default='noob')

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.post.id})


