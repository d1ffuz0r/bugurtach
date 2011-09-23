# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, get_user
from django.http import HttpResponseRedirect
from bugurtach.forms import EditBugurt
from bugurtach.models import CustomUser, Tag
from decorators import render_to
from django.db.models import Max
from models import Bugurt
from forms import AddBugurt

@render_to('home.html')
def homepage(request):
    bugurts = Bugurt.objects.order_by('-date')
    comments = [{'title':'text static comment', 'url': '/bugurts/1#1'}]
    top = bugurts.all().aggregate(Max('likes'))
    return {'title': 'homepage',
            'bugurts': bugurts,
            'latest_bugurts': bugurts.order_by('-date')[:10],
            'latest_comments': comments,
            'top_bugurt': top,
            'tags': Tag.all()}

@login_required(login_url="/login/")
@render_to('settings.html')
def user_settings(request):
    form = PasswordChangeForm
    return {'form': form}

@render_to('registration/registration.html')
def registration(request):
    if  request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm
    return {'reg_form': form}

@render_to('bugurts/bugurts.html')
def all_bugurts(request):
    bugurts = Bugurt.objects.order_by('-date')
    return {'bugurts': bugurts}

@login_required(login_url="/login/")
@render_to('bugurts/add.html')
def add_bugurt(request):
    if request.method == 'POST':
        form = AddBugurt(request.POST, {'author': CustomUser.objects.get(pk=get_user(request).id)})
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/user/%s/' % request.user)
    else:
        form = AddBugurt
    return {'add_form': form}

@login_required(login_url="/login/")
@render_to('bugurts/edit.html')
def edit_bugurt(request, name):
    bugurt = Bugurt.get_by_name(name)
    if request.user.username == bugurt.author.user.username:
        edit_form = EditBugurt({'name':bugurt.name, 'text':bugurt.text})
        return {'edit_form': edit_form}
    else:
        return HttpResponseRedirect(bugurt.get_absolute_url())

@login_required(login_url="/login/")
def delete_bugurt(request, bugurt):
    return {'static': bugurt}

@render_to('bugurts/view.html')
def view_bugurt(request, bugurt):
    return {'bugurt': Bugurt.get_by_name(bugurt)}

@render_to('bugurts/bugurts.html')
def view_user(request, username):
    return {'bugurts': Bugurt.get_by_author(username)}

@render_to('bugurts/bugurts.html')
def view_tags(request, tag):
    return {'bugurts': Bugurt.get_by_tag(tag)}
