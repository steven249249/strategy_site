from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class User(models.Model):
	name=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	info=RichTextField(blank=True,null=True)
	def __str__(self):
		return self.name

class Board(models.Model):
	name=models.CharField(max_length=100)
	content=models.CharField(max_length=100)
	def __str__(self):
		return self.name

class Post(models.Model):
	title=models.CharField(max_length=100)
	content=RichTextField(blank=True,null=True)
	like_count=models.PositiveIntegerField(default=0)
	board=models.ForeignKey(Board,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	pub_time=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class Message(models.Model):
	board=models.ForeignKey(Board,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	time=models.DateTimeField(auto_now=True)	

class Share(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	post=models.ForeignKey(Post,on_delete=models.CASCADE)

class Moderator(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	board=models.OneToOneField(Board,on_delete=models.CASCADE)

class BanList(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	board=models.ForeignKey(Board,on_delete=models.CASCADE)

class Collected(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	board=models.ForeignKey(Board,on_delete=models.CASCADE)	

class Like(models.Model):
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	user=models.ForeignKey(User,on_delete=models.CASCADE)	
	like=models.BooleanField(default=False)

class Comment (models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	content=models.CharField(max_length=10000)

class Inform(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	content=models.CharField(max_length=1000)
	pub_time=models.DateTimeField(auto_now=True)

class ChatMsg(models.Model):
	user = models.CharField(max_length=100)
	msg =  models.CharField(max_length=1000)
	board = models.CharField(max_length=100)
	send_time = models.DateTimeField()
	class Meta:
		app_label = 'chat'
		db_table = 'hamlet_chatmsg'