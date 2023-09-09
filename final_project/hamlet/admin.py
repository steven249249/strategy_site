from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display=('name','info')

class BoardAdmin(admin.ModelAdmin):
	list_display=('name','content')

class PostAdmin(admin.ModelAdmin):
	list_display=('title','like_count','id')
	ordering=('-pub_time',)

class MessageAdmin(admin.ModelAdmin):
	list_display=('board','user','time')
	ordering=('-time',)

class ShareAdmin(admin.ModelAdmin):
	list_display=('user','post')

class ModeratorAdmin(admin.ModelAdmin):
	list_display=('user','board')

class BanListAdmin(admin.ModelAdmin):
	list_display=('user','board')

class CollectedAdmin(admin.ModelAdmin):
	list_display=('user','board')

class LikeAdmin(admin.ModelAdmin):
	list_display=('post','user','like')

class InformAdmin(admin.ModelAdmin):
	list_display=('user','content','pub_time')
	ordering=('-pub_time',)

class CommentAdmin(admin.ModelAdmin):
	list_display=('user','post','content','id')

class ChatMessageAdmin(admin.ModelAdmin):
	list_display=('user','msg','board','send_time')
	ordering=('-send_time',)

admin.site.register(User,UserAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Board,BoardAdmin)
admin.site.register(Message,MessageAdmin)
admin.site.register(Share,ShareAdmin)
admin.site.register(Moderator,ModeratorAdmin)
admin.site.register(BanList,BanListAdmin)
admin.site.register(Collected,CollectedAdmin)
admin.site.register(Like,LikeAdmin)
admin.site.register(Inform,InformAdmin)
admin.site.register(ChatMsg,ChatMessageAdmin)



