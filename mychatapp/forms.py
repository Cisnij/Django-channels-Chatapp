from django import forms
from .models import Message,Profile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#mục đích tạo forms.py là để thao tác trực tới với csdl mà k cần phải tạo view get or create, và nó tự động validate dữ liệu có trông' hay không

class ChatMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['mess']  # Chỉ định các trường bạn muốn hiển thị trong form
        widgets = {
            'mess': forms.Textarea(attrs={'placeholder': 'Nhập tin nhắn...'}),  # Thay đổi kiểu hiển thị của trường mess
            
        }
        labels = {
            'mess': '',  # Label mới cho trường 'content'
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields=['name','pic']
