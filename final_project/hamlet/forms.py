from django import forms
from ckeditor.fields import RichTextField
from hamlet import models

class AddPostForm(forms.ModelForm):
	class Meta:
		model=models.Post
		fields=['title','content']
	def __init__(self,*args,**kwargs):
		super(AddPostForm,self).__init__(*args,**kwargs)
		self.fields['title'].label='標題'
		self.fields['content'].label='內容'

class UserForm(forms.ModelForm):
	class Meta:
		model=models.User 
		fields=['name','password']
		widgets = {
            'name': forms.TextInput(attrs={'class': "w3-input"}),
            'password': forms.TextInput(attrs={'class': "w3-input"}),

        }

	def __init__(self,*args,**kwargs):#看他是單一種變數*arg還是多種變數**kwargs
		super(UserForm,self).__init__(*args,**kwargs)
		self.fields['name'].label='帳號'
		self.fields['password'].label='密碼'

class PostForm(forms.ModelForm):
	class Meta:
		model=models.Post
		fields=['title','content']
	def __init__(self,*args,**kwargs):#看他是單一種變數*arg還是多種變數**kwargs
		super(PostForm,self).__init__(*args,**kwargs)
		self.fields['title'].label='標題'
		self.fields['content'].label='內容'

class CommentForm(forms.ModelForm):
	class Meta:
		model=models.Post
		fields=['content']


	def __init__(self,*args,**kwargs):#看他是單一種變數*arg還是多種變數**kwargs
		super(CommentForm,self).__init__(*args,**kwargs)
		self.fields['content'].label='內容'
		
class AlterForm(forms.ModelForm):
	class Meta:
		model=models.User
		fields=['info']
	def __init__(self, *arg, **kwargs):
		super(AlterForm, self).__init__(*arg, **kwargs)
		self.fields['info'].label='個人簡介'