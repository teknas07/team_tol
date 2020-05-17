from django.shortcuts import render
from chatapp.models import User, Message, Group, GroupMessage, GroupMember
import operator
from itertools import chain
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .forms import SendMessage, CreateGroup, SendMessageToGroup
from django.http import HttpResponseRedirect
from django.http import HttpResponse

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    num_users = User.objects.filter(is_superuser=False).count()
    current_user = request.user
    curr_name = current_user.first_name

    first_char = curr_name[0]

    group = Group.objects.all()
    group_name_list =[]
    for g in group:
        group_name_list.append(g.name)

    group_dict = {}
    for objs in group:
        group_dict[objs.name] = objs.id

    x = Message.objects.filter(to_user_id=current_user).order_by('-id')
    y = Message.objects.filter(from_user_id=current_user).order_by('-id')

    result_list = list(chain(x, y))
    result_list.sort(key=operator.attrgetter('id'), reverse=True)

    list1=[]
    for obj in result_list:
        list1.append(obj.from_user_id.username)
        list1.append(obj.to_user_id.username)

    unique_list = []

    def unique(list):
        for name in list:
            if name not in unique_list and name != current_user.username:
                unique_list.append(name)
    unique(list1)

    context = {
        'num_users': num_users,
        'curr_name': curr_name,
        'result_list': result_list,
        'unique_list': unique_list,
        'group_name_list' : group_name_list,
        'group_dict' : group_dict,
        'first_char': first_char,
    }

    return render(request, 'index.html', context=context)

def conversation(request,obj):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    name =obj #sent by
    to_user_obj = User.objects.get(username = name)
    current_user = request.user
    curr_name = current_user.username #recieved and sent by

    x = Message.objects.filter(to_user_id=current_user).order_by('-id')
    y = Message.objects.filter(from_user_id=current_user).order_by('-id')
    result_list = list(chain(x, y))
    result_list.sort(key=operator.attrgetter('id'), reverse=False)

    new_list=[]
    for item in result_list:
        if item.from_user_id.username == name and item.to_user_id.username == curr_name:
            new_list.append(item)
        elif item.from_user_id.username == curr_name and item.to_user_id.username == name:
            new_list.append(item)


    group = Group.objects.all()
    group_list = []
    for objs in group:
        group_list.append(objs.name)


    #form code
    #
    #
    form = SendMessage(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.from_user_id = request.user
        message.to_user_id = to_user_obj
        message.save()
        return HttpResponseRedirect(request.path_info)

    context ={
        'curr_name': curr_name,
        'name': name,
        'new_list':new_list,
        'result_list':result_list,
        'form': form,
        'group_list' : group_list,
    }

    return render(request,'conversation.html',context=context)

def createGroup(request):
    if request.user.is_staff:
        form1 = CreateGroup(request.POST)
        # form2 = AddMember(request.POST)

        if form1.is_valid():

            create_group = form1.save(commit = False)
            # add_member = form2.save(commit= False)

            # create_group.id = id
            # add_member.group_id = id
            create_group.save()
        current_user = request.user
        curr_name = current_user.username
    context = {
        'curr_name': curr_name,
        'form1' : form1,
    }
    return render(request,'createGroup.html',context=context)

def groupDetail(request, gid):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # group_id = gid
    group_obj = Group.objects.get(id = gid)
    group_name = group_obj.name

    group_message_obj = GroupMessage.objects.filter(to_user_id = group_obj)
    x = GroupMessage.objects.filter(to_user_id = group_obj)
    #x = Message.objects.filter(to_user_id=current_user).order_by('-id')
    mesg_list =[]
    for item in x:
        mesg_list.append(item.text)

    new_dict1 = {}
    for item in x:
        new_dict1[item.from_user_id] = item.text

    form = SendMessageToGroup(request.POST)
    if form.is_valid():
        message = form.save(commit=False)
        message.to_user_id = group_obj
        message.from_user_id = request.user
        message.save()
        return HttpResponseRedirect(request.path_info)

    all_users = User.objects.all()
    user_list = []
    for item in all_users:
        user_list.append(item.username)

    dict1 = {}
    group_objects = GroupMember.objects.filter(group_id = gid)
    group_members = []
    for item in group_objects:
        u_name = User.objects.get(username = item.user_id.username)
        group_members.append(u_name.first_name)
        f_letter = u_name.first_name[0]
        dict1[u_name] = f_letter

    # qset = GroupMember.objects.create(group_id = group_object, user_id = user_object)

    group = Group.objects.all()
    group_name_list = []
    for g in group:
        group_name_list.append(g.name)

    context ={
        'group_name' : group_name,
        'group_message_obj' : group_message_obj,
        'mesg_list' : mesg_list,
        'form': form,
        'user_list': user_list,
        'gid' : gid,
        'new_dict1' : new_dict1,
        'group_members' : group_members,
        'dict1' : dict1,
        'group_name_list' : group_name_list,
    }

    return render(request, 'groupDetail.html', context=context)

def AddMemberToGroup(request, gid):
    # form1 = AddMember(request.POST)
    # if form1.is_valid():
    #     sel_user = form1.save(commit=False)
    #     answer = request.GET.get('selected_user')
    #     qset = User.objects.get(username = answer)
    #     sel_user.user_id = qset.id
    #     sel_user.group_id = gid
    #     sel_user.save()
    #     return HttpResponseRedirect(request.path_info)
    selected_user = request.POST.get('selected_user')
    # GroupMember.group_id = gid
    # GroupMember.user_id = qset.id
    user_object = User.objects.get(username = selected_user)
    group_object = Group.objects.get(id = gid)
    qset = GroupMember.objects.create(group_id=group_object, user_id=user_object )
    qset.save()
    # return HttpResponse('done')
    context = {
        'selected_user': selected_user,
    }
    return render(request, 'user_added.html', context)