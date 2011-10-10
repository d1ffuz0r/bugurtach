# -*- coding: utf-8 -*-
from bugurtach.models import Tag, Comments, Bugurt
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from bugurtach.forms import EditBugurt, AddTag, AddProof, AddBugurt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from decorators import render_to


@render_to("home.html")
def homepage(request):
    return {"tags": Tag.all(),
            "top_bugurts": Bugurt.top(),
            "latest_bugurts": Bugurt.latest(),
            "latest_comments": Comments.latest_comments()}

@login_required(login_url="/login/")
@render_to("settings.html")
def user_settings(request):
    msg = ""
    if request.POST:
        form_password = PasswordChangeForm(request.user, request.POST)
        if form_password.is_valid():
            form_password.save()
            msg = "СХОРОНИЛ!"
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
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"]
            )
            login(request, user)
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm
    return {"reg_form": form}

@render_to("bugurts/bugurts.html")
def all_bugurts(request):
    return {"bugurts": Bugurt.all()}

@login_required(login_url="/login/")
@render_to("bugurts/add.html")
def add_bugurt(request):
    user = request.user
    if request.method == "POST":
        form = AddBugurt(request.POST, initial={"author": user})
        if form.is_valid():
            Bugurt.create_bugurt(form=form, user=user)
            return HttpResponseRedirect("/user/%s/" % user)
    else:
        form = AddBugurt()
    return {"add_form": form}

@login_required(login_url="/login/")
@render_to("bugurts/edit.html")
def edit_bugurt(request, name):
    bugurt = Bugurt.get_by_name(name)
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
    bugurt = Bugurt.get_by_name(name)
    if request.user.username == bugurt.author.username:
        bugurt.delete()
        return HttpResponseRedirect("/user/%s/" % request.user)
    else:
        return HttpResponseRedirect("/")

@render_to("bugurts/view.html")
def view_bugurt(request, bugurt):
    bugurt_obj = Bugurt.get_by_name(bugurt)
    if bugurt_obj:
        return {"bugurt": bugurt_obj}
    else:
        raise Http404

@render_to("bugurts/bugurts.html")
def view_user(request, username):
    bugurt_objects = Bugurt.get_by_author(username)
    if bugurt_objects:
        return {"bugurts": bugurt_objects}
    else:
        return Http404

@render_to("bugurts/bugurts.html")
def view_tags(request, tag):
    return {"bugurts": Bugurt.get_by_tag(tag)}

@render_to("tags.html")
def view_all_tags(request):
    return {"tags": Tag.all()}
