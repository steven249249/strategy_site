from django.shortcuts import render
from . import models
# Create your views here.
from . import forms
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.http import HttpResponse, JsonResponse
import datetime


def login(request):
	if request.method=='POST':
		form=forms.UserForm(request.POST)
		if form.is_valid():
			name=request.POST['name']
			password=request.POST['password']
			try:
				user=models.User.objects.get(name=name)
				if password==user.password:
					request.session['name']=name
					request.session['id']=user.id
					messages.add_message(request,messages.WARNING,"登入成功")
					return redirect('/board_all/')
				else:
					messages.add_message(request,messages.WARNING,"密碼不正確")
			except:
				messages.add_message(request,messages.WARNING,"找不到使用者")
		else:	
			messages.add_message(request,messages.WARNING,"請填滿欄位")

	else:
		form=forms.UserForm()

	return render(request,'login.html',locals())


def logout(request):

	if 'name' in request.session and 'id' in request.session:
		Session.objects.all().delete()

	return redirect('/login/')


def board_all(request,page=1):

	if 'id' in request.session:
		loginid=request.session['id']
	if 'name' in request.session:
		name=request.session['name']


	board_all=models.Board.objects.all()
	board_spilt=[board_all[i:i + 4] for i in range(0, len(board_all), 4)]
	pages=range(1,len(board_spilt)+1)
	
	if (page<len(board_spilt)+1) and page>0:
		boards=board_spilt[page-1]
	else:
		messages.add_message(request,messages.WARNING,"指定頁數不存在")

	return render(request,'board_all.html',locals())

def board(request, board_name=None, page=1):
	try:
		board = models.Board.objects.get(name=board_name)
	except:
		return redirect('board_all')
	if('name' in request.session):
		name=request.session['name']
		user = models.User.objects.get(name=name)
		try:
			banned = models.BanList.objects.get(user=user, board=board)
		except:
			banned = None
		if(request.GET.get('method', False)):
			if(request.GET['method']=='collect'):
				collected = models.Collected.objects.create(user=user, board=board)
				collected.save()
				messages.add_message(request,messages.SUCCESS,"已成功收藏此板")
			if(request.GET['method']=='decollect'):
				try:
					collected = models.Collected.objects.get(user=user, board=board)
					collected.delete()
					messages.add_message(request,messages.SUCCESS,"已取消收藏此板")
				except:
					pass
			redirect_url = '/board/' + board.name
			return redirect(redirect_url)
		try:
			collected = models.Collected.objects.filter(user__name=name, board=board)
		except:
			collected = None
	else:
		name = None
	try:
		moderator = models.Moderator.objects.get(board=board)
	except:
		moderator = None
	page = page
	try:
		posts = models.Post.objects.filter(board=board).order_by('-pub_time')
	except:
		posts = None
	if(posts):
		num_in_page = 10
		posts_split = [posts[i:i+num_in_page] for i in range(0, len(posts), num_in_page)]
		num_of_pages = len(posts_split)
		pages = range(1, num_of_pages+1)
		if(page<=num_of_pages and page>0):
			posts = posts_split[page-1]
		else:
			messages.add_message(request,messages.WARNING,"指定頁數不存在")
	return render(request, 'board.html', locals())

def add_post(request, board_name=None):
	if('name' in request.session):
		name=request.session['name']
		user = models.User.objects.get(name=name)
	else:
		messages.add_message(request,messages.WARNING,"請先登入才能新增文章喔！")
		return redirect('/login')
	try:
		board = models.Board.objects.get(name=board_name)
	except:
		return redirect('board_all')
	try:
		banned = models.BanList.objects.get(user=user, board=board)
	except:
		banned = None
	if(banned):
		messages.add_message(request,messages.WARNING,"你已在此板被Ban，無法發文！")
		redirect_url = '/board/' + board.name
		return redirect(redirect_url)
	if(request.method=='POST'):
		add_post_form = forms.AddPostForm(request.POST)
		if(add_post_form.is_valid()):
			new_post = models.Post(board=board, user=user)
			add_post_form = forms.AddPostForm(request.POST, instance=new_post)
			add_post_form.save()
			messages.add_message(request,messages.WARNING,"文章已新增完成！")
			collected_list = models.Collected.objects.filter(board=board)
			for collect in collected_list:
				targer_user = collect.user
				inform_msg = "你收藏的板<a class='w3-text-blue' href='/board/"+board.name+"'>"+board.name+"</a>有新文章"
				new_inform = models.Inform.objects.create(user=targer_user, content=inform_msg)
				new_inform.save()
			redirect_url = '/board/' + board.name
			return redirect(redirect_url)
		else:
			messages.add_message(request,messages.WARNING,"請填寫完整！")
	else:
		add_post_form = forms.AddPostForm()
	return render(request, 'add_post.html', locals())

def send_msg(request):
	try:
		msg = request.POST['msg']
		user = request.POST['user']
		board_name = request.POST['board_name']
	except:
		messages.add_message(request,messages.WARNING,"非法操作！")
		return redirect('/board_all')
	datetime_dt = datetime.datetime.today()
	time_delta = datetime.timedelta(hours=8)
	new_dt = (datetime_dt + time_delta)
	new_msg = models.ChatMsg.objects.create(user=user, board=board_name, msg=msg, send_time=new_dt)
	new_msg.save()
	return HttpResponse('Message send successfully')

def get_msg(request, board_name=None):
	try:
		name=request.session['name']
		msgs = models.ChatMsg.objects.filter(board=board_name).order_by('send_time')
		for msg in msgs:
			msg.send_time = msg.send_time.strftime("%Y/%m/%d %H:%M:%S")
			
		print(msgs[0].send_time)
		return JsonResponse({"msgs":list(msgs.values()),"user_name":name})
	except:
		return HttpResponse(None)

def post(request,postid):
	if 'name' in request.session:
		name=request.session['name']


	try:
		post=models.Post.objects.get(id=postid)
		comments=models.Comment.objects.filter(post=post)
	except:
		messages.add_message(request,messages.WARNING,'找不到此貼文')
		return redirect('/board_all/')

	try:
		if name:
			user_=models.User.objects.get(name=name)
			ban=models.BanList.objects.get(user=user_,board=post.board)			
		else:
			ban=''
	except:
		pass


	try:
		if name:
			if name == post.user.name:
				verified=True
			else:
				verified=False

		else:
			verified=False
	except:
		pass 
	if request.method=='POST' and 'like' in request.POST:
		try:
			user=models.User.objects.get(name=name)
			like=models.Like.objects.get(post=post,user=user)
			if like.like==True:
				like.like=False
				like.save()
				post.like_count-=1
				post.save()
			else:
				like.like=True
				like.save()
				post.like_count+=1
				post.save()
		except:
			like=models.Like.objects.create(post=post,user=user,like=True)
			post.like_count+=1
			post.save()


	if request.method=='POST' and 'comment' in request.POST:
		user=models.User.objects.get(name=name)
		comment=models.Comment.objects.create(user=user,post=post,content=request.POST['content'])
		comment.save()
		likes=models.Like.objects.filter(post=post)
		users_like=[]
		for like in likes:
			users_like.append(like.user)
		for users in users_like:
			contents="你喜歡的文章:<a class='w3-text-blue' href='/post/"+str(post.id)+"'>"+post.title+"</a>有新留言"
			informs=models.Inform.objects.create(user=users,content=contents)
			informs.save()
	
	return render(request,'post.html',locals())



def share(request,postid):
	
	if 'name' in request.session:
		name=request.session['name']
		user=models.User.objects.get(name=name)
		post=models.Post.objects.get(id=postid)
		share=models.Share.objects.create(user=user,post=post)
		share.save()
		messages.add_message(request,messages.SUCCESS,'分享成功')
		return redirect('/post/{}'.format(postid))
	else:
		return redirect('/login/')

def remove(request,postid):
	if 'name' in request.session:
		try:
			name=request.session['name']
			post=models.Post.objects.get(id=postid)
			if post.user.name==name:
				post.delete()
				messages.add_message(request,messages.WARNING,'刪除成功')
			else:
				messages.add_message(request,messages.WARNING,'你不能刪除別人的貼文')

			return redirect('/board/{}'.format(post.board.name))
		except:
			messages.add_message(request,messages.WARNING,'找不到該貼文')
			return redirect('/board_all/')

	else:
		return redirect('/login/')

def alter_post(request,postid):
	if 'name' in request.session:
		try:
			name=request.session['name']
			post=models.Post.objects.get(id=postid)
			if post.user.name==name:
				verified=True
				if request.method=='POST':
					form=forms.PostForm(request.POST,instance=post)
					if form.is_valid():
						form.save()
						messages.add_message(request,messages.WARNING,'修改成功')

					return redirect('/post/{}'.format(postid))
				else:
					form=forms.PostForm(initial={'title':post.title,'content':post.content})
				
			else:
				verified=False
				messages.add_message(request,messages.WARNING,'你不能修改別人的貼文')
				return redirect('/post/{}'.format(postid))	
		except:
			messages.add_message(request,messages.WARNING,'找不到該文章')


		try:
			if name:
				user_=models.User.objects.get(name=name)
				ban=models.BanList.objects.get(user=user_,board=post.board)
				messages.add_message(request,messages.WARNING,'你被該板ban了,不能修改你的貼文,但可以刪除')
				return redirect('/board_all/')			
			else:
				ban=''
		except:
			pass

	else:
		return redirect('/login/')

	return render(request,'alter_post.html',locals())

def alter_comment(request,commentid):
	if 'name' in request.session:
		try:
			name=request.session['name']
			comment=models.Comment.objects.get(id=commentid)
			postid=comment.post.id
			post=models.Post.objects.get(id=postid)
			if comment.user.name==name:
				verified=True
				if request.method=='POST':
					form=forms.CommentForm(request.POST,instance=comment)
					if form.is_valid():
						form.save()
						messages.add_message(request,messages.WARNING,'修改成功')

					return redirect('/post/{}'.format(postid))
				else:
					form=forms.CommentForm(initial={'content':comment.content})
				
			else:
				verified=False
				messages.add_message(request,messages.WARNING,'你不能修改別人的留言')
				return redirect('/post/{}'.format(postid))
		except:
			messages.add_message(request,messages.WARNING,'找不到該留言')
			
		try:
			if name:
				user_=models.User.objects.get(name=name)
				ban=models.BanList.objects.get(user=user_,board=post.board)
				messages.add_message(request,messages.WARNING,'你被該板ban了,不能修改你的回覆,但可以刪除')
				return redirect('/post/{}'.format(postid))			
			else:
				ban=''
		except:
			pass

	else:
		return redirect('/login/')

	return render(request,'alter_comment.html',locals())

def remove_comment(request,commentid):
	if 'name' in request.session:
		try:
			name=request.session['name']
			comment=models.Comment.objects.get(id=commentid)
			postid=comment.post.id
			if comment.user.name==name:
				comment.delete()
				messages.add_message(request,messages.WARNING,'刪除成功')
			else:
				messages.add_message(request,messages.WARNING,'你不能刪除別人的留言')

			return redirect('/post/{}'.format(postid))
		except:
			messages.add_message(request,messages.WARNING,'找不到該留言')
			return redirect('/board_all/')

	else:
		return redirect('/login/')

def home(request,userid=0):
	
	if 'name' in request.session:
		name=request.session['name']
	if 'id' in request.session:
		loginid=request.session['id']
		if userid==0:
			userid=loginid
			return redirect('/home/{}'.format(loginid))
	else:
		loginid=None

	try:
		mod=models.Moderator.objects.get(user_id=loginid)
	except:
		mod=None

	try:
		userinfo=models.User.objects.get(pk=userid)
	except:
		userinfo=None
			
	try:
		userinfor=models.User.objects.filter(pk=userid)
	except:
		userinfor=None

	try:
		banlist=models.BanList.objects.get(user_id=userid,board=mod.board)
	except:
		banlist=None



	# try:
	# 	moderator=models.Moderator.objects.all()
	# except:
	# 	moderator=None

	# try:
	# 	banlist=models.BanList.objects.filter(user=userinfo)
	# except:
	# 	banlist=None

	# try:
	# 	ban=request.GET['ban']
	# except:
	# 	ban='None'

	# if ban!=None:
	# 	for mod in moderator:
	# 		if name == mod.user.name:
	# 			banned=models.BanList.objects.create(user=userinfo,board=mod.board)
	# 			banned.save()
	# else:
	# 	for mod in moderator:
	# 		if name == mod.user.name:
	# 			banned=models.BanList.objects.filter(user=userinfo,board=mod.board)
	# 			if banned:
	# 				banned.delete()


	return render(request,'home.html',locals())

def alter(request,userid):
	try:
		userinfo=models.User.objects.get(pk=userid)
	except:
		userinfo=None
	if 'name' in request.session:
		name=request.session['name']
		userdata=models.User.objects.get(name=name)

		if request.method=="POST":
			form=forms.AlterForm(request.POST,instance=userdata)
			if form.is_valid():
				form.save()
				message="修改成功"
				return redirect('/home/{}'.format(userid))
			else:
				message="修改失敗"
		else:
			form=forms.AlterForm(initial={'info':userdata.info})

	return render(request,'alter.html',locals())

def collected(request,userid):
	if 'name' in request.session:
		name=request.session['name']
	if 'id' in request.session:
		loginid=request.session['id']

	userinfo=models.User.objects.get(pk=userid)
	usercollect=models.Collected.objects.filter(user=userid)
	return render(request,'collected.html',locals())

def sharelist(request,userid):
	if 'name' in request.session:
		name=request.session['name']
	if 'id' in request.session:
		loginid=request.session['id']

	userinfo=models.User.objects.get(pk=userid)
	usershare=models.Share.objects.filter(user=userid)
	return render(request,'share.html',locals())

def inform(request,userid):
	if 'name' in request.session:
		name=request.session['name']
	if 'id' in request.session:
		loginid=request.session['id']

	userinfo=models.User.objects.get(pk=userid)
	userinform=models.Inform.objects.filter(user=userid)
	return render(request,'inform.html',locals())

def register(request):

    if request.method=='POST':
        form=forms.UserForm(request.POST)
        if form.is_valid():
            name=request.POST['name']
            password=request.POST['password']
            try:
                user=models.User.objects.get(name=name)
                messages.add_message(request,messages.WARNING,"該名字已註冊")
            except:
                user=models.User.objects.create(name=name,password=password)
                user.save()
                messages.add_message(request,messages.WARNING,"成功註冊")
                return redirect('/login/')
        else:
            messages.add_message(request,messages.WARNING,"請填滿欄位")

    else:
        form=forms.UserForm()

    return render(request,'register.html',locals())

def ban(request,userid):
	if 'name' in request.session:
		name=request.session['name']
	else:
		name=None

	if 'id' in request.session:
		loginid=request.session['id']
		if loginid==userid:
			messages.add_message(request,messages.WARNING,'不可以ban自己')
			return redirect('/home/{}'.format(userid))

		else:
			try:
				mod=models.Moderator.objects.get(user_id=loginid)
			except:
				messages.add_message(request,messages.SUCCESS,'您並非板主')
				return redirect('/home/{}'.format(userid))

			try:
				banlist=models.BanList.objects.get(user_id=userid,board=mod.board)
				banlist.delete()
				messages.add_message(request,messages.SUCCESS,'已解ban該使用者')
				return redirect('/home/{}'.format(userid))
			except:
				user=models.User.objects.get(pk=userid)
				unban=models.BanList.objects.create(user=user,board=mod.board)
				unban.save()
				messages.add_message(request,messages.SUCCESS,'已ban掉該使用者')
				return redirect('/home/{}'.format(userid))