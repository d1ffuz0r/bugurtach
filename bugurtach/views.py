# -*- coding: utf-8 -*-
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from bugurtach.models import Tag, Comments, Bugurt
from bugurtach.forms import EditBugurt, AddTag, AddProof, AddBugurt
from decorators import render_to


@render_to("home.html")
def homepage(request):
    return {"tags": Tag.all(),
            "top_bugurts": Bugurt.manager.top(),
            "latest_bugurts": Bugurt.manager.latest(),
            "latest_comments": Comments.latest_comments()}

@login_required(login_url="/login/")
@render_to("settings.html")
def user_settings(request):
    msg = ""
    if request.POST:
        form_password = PasswordChangeForm(request.user, request.POST)
        if form_password.is_valid():
            msg = True
            form_password.save()
    else:
        form_password = PasswordChangeForm(request.user)
    return {"form_password": form_password,
            "msg": msg}

@render_to("registration/registration.html")
def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password1"])
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm
    return {"reg_form": form}

@render_to("bugurts/bugurts.html")
def all_bugurts(request):
    return {"bugurts": Bugurt.manager.all()}

@render_to("bugurts/bugurts.html")
def top_bugurts(request):
    return {"bugurts": Bugurt.manager.top()}

@login_required(login_url="/login/")
@render_to("bugurts/add.html")
def add_bugurt(request):
    user = request.user
    if request.method == "POST":
        form = AddBugurt(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/user/%s/" % user)
    else:
        form = AddBugurt()
    return {"add_form": form}

@login_required(login_url="/login/")
@render_to("bugurts/edit.html")
def edit_bugurt(request, name):
    bugurt = Bugurt.manager.get_by_name(name)
    if request.user.username == bugurt.author.username:
        if request.POST:
            edit_form = EditBugurt(request.POST)
            if edit_form.is_valid():
                bugurt.name = edit_form.cleaned_data["name"]
                bugurt.text = edit_form.cleaned_data["text"]
                bugurt.save()
                return HttpResponseRedirect(bugurt.get_absolute_url())
        else:
            edit_form = EditBugurt(initial={"name": bugurt.name, "text": bugurt.text})
        return {"edit_form": edit_form,
                "bugurt": bugurt,
                "tag_add": AddTag(),
                "proof_add": AddProof()}
    else:
        return HttpResponseRedirect(bugurt.get_absolute_url())

@login_required(login_url="/login/")
def delete_bugurt(request, name):
    bugurt = Bugurt.manager.get_by_name(name)
    if request.user.username == bugurt.author.username:
        bugurt.delete()
        return HttpResponseRedirect("/user/%s/" % request.user)
    else:
        return HttpResponseRedirect("/")

@render_to("bugurts/view.html")
def view_bugurt(request, bugurt):
    bugurt_obj = Bugurt.manager.get_by_name(bugurt)
    if bugurt_obj:
        return {"bugurt": bugurt_obj}
    else:
        return {"bugurt": ""}

@render_to("bugurts/bugurts.html")
def view_user(request, username):
    bugurt_objects = Bugurt.manager.get_by_author(username)
    if bugurt_objects:
        return {"bugurts": bugurt_objects}
    else:
        return {"bugurts": None}

@render_to("bugurts/bugurts.html")
def view_tags(request, tag):
    return {"bugurts": Bugurt.manager.get_by_tag(tag)}

@render_to("tags.html")
def view_all_tags(request):
    return {"tags": Tag.all()}
