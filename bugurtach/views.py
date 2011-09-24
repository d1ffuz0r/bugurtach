# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from bugurtach.forms import EditBugurt
from bugurtach.models import Tag, BugurtTags
from decorators import render_to
from models import Bugurt
from forms import AddBugurt

@render_to('home.html')
def homepage(request):
    bugurts = Bugurt.objects.order_by('-id')
    top_bugurt = Bugurt.objects.order_by('-likes').order_by('-comments')[:1]
    return {'title': 'homepage',
            'bugurts': bugurts,
            'top_bugurt': top_bugurt,
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
        form = AddBugurt(request.POST, {'author': request.user})
        if form.is_valid():
            data = form.data
            tag_names = data['tags'].replace(' ,',',').replace(', ',',').split(',')
            bugurt = Bugurt.objects.create(name=data['name'],
                                           author=request.user,
                                           text=data['text'])
            tt = []
            for name in tag_names:
                tag = Tag.objects.filter(title=name)
                if tag:
                    t = Tag.objects.get(title=name)
                    BugurtTags(bugurt=bugurt, tag=t).save()
                    tt.append(t)
                else:
                    t = Tag.objects.create(title=name)
                    BugurtTags(bugurt=bugurt, tag=t).save()
                    tt.append(t)
            bugurt.tags_set = tt
            bugurt.save()
            return HttpResponseRedirect('/user/%s/' % request.user)
    else:
        form = AddBugurt
    return {'add_form': form}

@login_required(login_url="/login/")
@render_to('bugurts/edit.html')
def edit_bugurt(request, name):
    bugurt = Bugurt.get_by_name(name)
    if request.user.username == bugurt.author.username:
        if request.POST:
            edit_form = EditBugurt(request.POST)
            if edit_form.is_valid():
                bugurt.name = edit_form.cleaned_data['name']
                bugurt.text = edit_form.cleaned_data['text']
                bugurt.save()
        else:
            edit_form = EditBugurt({'name': bugurt.name, 'text': bugurt.text})
        return {'edit_form': edit_form}
    else:
        return HttpResponseRedirect(bugurt.get_absolute_url())

@login_required(login_url="/login/")
def delete_bugurt(request, name):
    bugurt = Bugurt.get_by_name(name)
    if request.user.username == bugurt.author.username:
        bugurt.delete()
        return HttpResponseRedirect("/user/%s/" % request.user)
    else:
        return HttpResponseRedirect('/')

@render_to('bugurts/view.html')
def view_bugurt(request, bugurt):
    return {'bugurt': Bugurt.get_by_name(bugurt)}

@render_to('bugurts/bugurts.html')
def view_user(request, username):
    return {'bugurts': Bugurt.get_by_author(username)}

@render_to('bugurts/bugurts.html')
def view_tags(request, tag):
    return {'bugurts': Bugurt.get_by_tag(tag)}
