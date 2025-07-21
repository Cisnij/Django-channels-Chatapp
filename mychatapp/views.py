from django.shortcuts import render,redirect
from .models import *
from .forms import ChatMessageForm,CreateUserForm,ProfileForm
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user.profile 
        friends = user.friends.all() 
        friend_request=AddFriend.objects.filter(receiver_request=user,status=False) # lấy ra danh sách yêu cầu kết bạn
        
    else:
        user = None
        friends = None  
        return redirect('login')  
    context={'user':user,'friends':friends,'friend_request':friend_request} 
    return render(request, 'mychatapp/index.html',context)


    
def detail(request,pk):
    friend = Friend.objects.get(profile__id=pk)
    user =request.user.profile
    friend_profile=Profile.objects.get(id=friend.profile.id)
    rec_chat=Message.objects.filter(receiver=user,sender=friend.profile) # lưu số count ngăn duplicate tin nhắn
    rec_chat.update(seen=True) #Khi người dùng click vào tin nhắn thì sẽ load detail path , và khi đó chỉ cần update 
    chat=Message.objects.all()
    form = ChatMessageForm()
    if request.method =='POST':
        form =ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message=form.save(commit=False)
            chat_message.sender=user
            chat_message.receiver=friend_profile
            chat_message.save()
            return redirect('detail',pk=friend.profile.id)

    context={'friend':friend,'form':form,'friend_profile':friend_profile,'user':user,'chat':chat,'num':rec_chat.count()}
    return render(request, 'mychatapp/detail.html',context)

def sendMessage(request,pk):
    user=request.user.profile
    friend= Friend.objects.get(profile__id=pk) # lay ra tat ca friend cua user co id= 
    data=json.loads(request.body) #lấy ra body của script trong detail html
    newchat= data['msg'] #lay ra data tu script
    message=Message.objects.create(mess=newchat,sender=user,receiver=friend.profile,seen=False) #tao ra message moi de hien thi len 
    context={'mess':message.mess,'avatar':request.user.profile.pic.url} #tao ra context de tra ve cho script
    return JsonResponse(context,safe=False)

def receiveMessage(request,pk):
    user=request.user.profile
    friend=Friend.objects.get(profile__id=pk)
    chat=Message.objects.filter(receiver=user,sender=friend.profile)
    arr=[] #tạo ra array để chứa các message hiển thị tóm tắt bên ngoài chat trước khi click vào chat
    for i in chat:
        arr.append(i.mess)  
    context={'message':arr,'avatar':friend.profile.pic.url} 
    return JsonResponse(context) #trả về arr cho script trong detail.html để hiển thị ra ngoài chat json=>data
    
#receiveMessage khác sendMessage là recieve là nhận xuống từ server và k phải tạo ra message trong database(filter), còn send là gửi lên server và tạo ra message trong database(create)

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method =='POST':
            username=request.POST.get("username")
            password=request.POST.get("password")    
            user=authenticate(request,username=username,password=password) #kiem tra xem username va password co ton tai trong csdl hay khong
            if user is not None: # neu co thi dang nhap
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,'Username or password không đúng !')
                return redirect('login')
    return render(request,'mychatapp/login.html')

def Logout(request):
    logout(request)
    return redirect('login')

def Register(request):  
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
           # Profile.objects.create(user=user,name=user.username)
            return redirect('login')
    context={'form':form}        
    return render(request,'mychatapp/register.html',context)    

from django.http import JsonResponse
from django.contrib import messages

def addFriend(request):
    user = request.user.profile
    messages_list = []

    if request.method == 'POST':
        search = request.POST.get('search', '')
        try:
            user_add = Profile.objects.get(id=search)
        except Profile.DoesNotExist:
            messages_list.append("Không tìm thấy người dùng này!")
            return JsonResponse({'messages': messages_list})

        if user_add == user:
            messages_list.append("Bạn không thể kết bạn với chính mình!")
            return JsonResponse({'messages': messages_list})

        if user.friends.filter(profile=user_add).exists():
            messages_list.append("Người này đã là bạn bè của bạn!")
            return JsonResponse({'messages': messages_list})

        if AddFriend.objects.filter(sender_request=user, receiver_request=user_add).exists():
            messages_list.append("Bạn đã gửi yêu cầu kết bạn đến người này!")
            return JsonResponse({'messages': messages_list})

        AddFriend.objects.create(sender_request=user, receiver_request=user_add, status=False)
        messages_list.append("Yêu cầu kết bạn đã được gửi đến người này!")

    return JsonResponse({'messages': messages_list})

    

        
def acceptFriend(request):
    # câu lệnh gợi ý bạn bè 
    # user.objects.exclude(friend__in= friend).exclude(user=user)
    if request.method=='POST':
        data=json.loads(request.body)
        action=data['action']
        id=data['friend_id']
        user=request.user.profile
        friend=Profile.objects.get(id=id) # (1)
        if action =='accept':
            AddFriend.objects.filter(sender_request=friend,receiver_request=user).delete() # xoa yeu cau ket ban

            friend_user, created =Friend.objects.get_or_create(profile=user) # thêm friend cho user
            friend_friend ,created=Friend.objects.get_or_create(profile=friend) # thêm friend cho friend 

            user.friends.add(friend_friend)
            friend.friends.add(friend_user) # từ friend ở (1)
            context={'status':'accepted'}
            return JsonResponse(context)
        if action=='reject':
            AddFriend.objects.filter(sender_request=friend,receiver_request=user).delete()
            context={'status':'rejected'}
            return JsonResponse(context)
    return JsonResponse({'status':'error'}, status=400) # trả về lỗi nếu không có yêu cầu kết bạn nào được tìm thấy        

def Notification(request):
    user=request.user.profile
    friend=user.friends.all() # lấy ra tat ca ban be cua user
    arr=[]
    for friends in friend:
        chat=Message.objects.filter(sender__id=friends.profile.id,receiver=user,seen=False)# lấy ra tất cả các tin nhắn chưa đọc của bạn bè
        arr.append(chat.count())
    return JsonResponse(arr,safe=False)

    
def ProfileUser(request):
    user=request.user.profile
    form=ProfileForm(instance=user) #lấy ra form của profile hiện tại
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=user)#lay ra nhung cai dc chinh sua va anh de update thong tin
        if form.is_valid():
            form.save()
            return redirect('profile')
    context={'user':user,'form':form}
    return render(request,'mychatapp/profile.html',context)
