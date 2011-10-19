# -*- coding: utf-8 -*-
from bugurtach.models import Bugurt, Comments, BugurtTags, Tag, Proof, BugurtProofs
from decorators import render_json, check_ajax
from django.http import HttpResponse
from django.utils.html import escape

def reply(request):
    random_reply = Comments.objects.order_by('?')[0].text
    return HttpResponse(random_reply)

@render_json
@check_ajax
def like(request):
    result = {}
    user = request.user
    bugurt_id = request.POST["bugurt_id"]
    type = request.POST["type"]
    if type == "like":
        like = Bugurt.manager.like(user, bugurt_id, "like")
        if like:
            result.update({"message": "Охуенно!",
                           "post": bugurt_id,
                           "likes": like})
        else:
            result.update({"message": "Вы уже голосовали за этот бугурт"})
    if type == "dislike":
        like = Bugurt.manager.like(user, bugurt_id, "dislike")
        if like:
            result.update({"message": "Хуита",
                           "post": bugurt_id,
                           "likes": like})
        else:
            result.update({"message": "Вы уже голосовали за этот бугурт"})
    return result

@render_json
@check_ajax
def add_comment(request):
    result = {}
    if request.POST["text"]:
        comment, created = Comments.objects.get_or_create(author=request.user,
                                                          bugurt=Bugurt.objects.get(id=request.POST["bugurt"]),
                                                          text=request.POST["text"])
        if created:
            result.update({"comment": {"id": comment.id,
                                       "author": comment.author.username,
                                       "text": escape(comment.text),
                                       "date": comment.date.strftime("%d.%m.%y, %H:%M")}})
            comment.save()
        else:
            result.update({"message": "Already exist"})
    else:
        result.update({"message":"Enter message please"})
    return result

@render_json
@check_ajax
def add_tag(request):
    result = {}
    bugurt = request.POST["bugurt"]
    tag = escape(request.POST["tag"])
    if tag:
        bugurt_obj = Bugurt.objects.get(id=bugurt)
        if bugurt_obj.author.username == request.user.username:
            t, created = Tag.objects.get_or_create(title=tag)
            btag = BugurtTags.objects.filter(bugurt=bugurt_obj, tag=t)
            if not btag:
                BugurtTags(bugurt=bugurt_obj, tag=t).save()
                result.update({"tag": t.title, "id": t.id})
            else:
                result.update({"message": "Already exist"})
        else:
            result.update({"message":"4itak dohuya?"})
    else:
        result.update({"message":"Enter name tag please"})
    return result

@render_json
@check_ajax
def delete_tag(request):
    bugurt = request.POST["bugurt"]
    tag = request.POST["tag"]
    BugurtTags.objects.filter(bugurt=bugurt, tag=tag).delete()
    return {"bugurt": bugurt, "tag": tag}

@render_json
@check_ajax
def add_proof(request):
    result = {}
    bugurt = request.POST["bugurt"]
    proof = escape(request.POST["proof"])
    if proof:
        bugurt_obj = Bugurt.objects.get(id=bugurt)
        if bugurt_obj.author.username == request.user.username:
            p, created = Proof.objects.get_or_create(link=proof)
            bproof = BugurtProofs.objects.filter(bugurt=bugurt_obj, proof=p)
            if not bproof:
                BugurtProofs(bugurt=bugurt_obj, proof=p).save()
                result.update({"proof": p.link, "id": p.id})
            else:
                result.update({"message": "Already exist"})
        else:
            result.update({"message":"4itak dohuya?"})
    else:
        result.update({"message":"Enter name proof please"})
    return result

@render_json
@check_ajax
def delete_proof(request):
    bugurt = request.POST["bugurt"]
    proof = request.POST["proof"]
    BugurtProofs.objects.filter(bugurt=bugurt, proof=proof).delete()
    return {"bugurt": bugurt, "proof": proof}

@check_ajax
def autocomplite(request):
    result = ''
    text = escape(request.POST["text"])
    tags = Tag.objects.filter(title__contains=text)
    for tag in tags:
        result += "<li>%s</li>" % tag.title
    return HttpResponse(result)

