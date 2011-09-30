# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.utils import simplejson
from bugurtach.models import Bugurt, Comments, BugurtTags, Tag, Proof, BugurtProofs
from django.utils.html import escape

def like(request):
    result = {}
    if request.user:
        if request.is_ajax():
            bugurt_id = request.POST['bugurt_id']
            type = request.POST['type']
            user = request.user
            if type == 'like':
                like = Bugurt.like(user, bugurt_id, 'like')
                if like:
                    result.update({'message': 'Охуенно!',
                                   'post': bugurt_id,
                                   'likes': like})
                else:
                    result.update({'message': 'Вы уже голосовали за этот бугурт'})
            if type == 'dislike':
                like = Bugurt.like(user, bugurt_id, 'dislike')
                if like:
                    result.update({'message': 'Хуита',
                                   'post': bugurt_id,
                                   'likes': like})
                else:
                    result.update({'message': 'Вы уже голосовали за этот бугурт'})
        else:
            result.update({'message':'WOK.'})
    else:
        result.update({'message':'Login please'})
    return HttpResponse(simplejson.dumps(result), 'json')

def add_comment(request):
    result = {}
    if request.user:
        if request.is_ajax():
            user = request.user
            bugurt = request.POST['bugurt']
            text = request.POST['text']
            if text:
                comment = Comments.objects.create(author=user,
                                                  bugurt=Bugurt.objects.get(id=bugurt),
                                                  text=text)
                result.update({'comment': {'id': comment.id,
                                           'author': comment.author.username,
                                           'text': escape(comment.text),
                                           'date': comment.date.strftime('%d.%m.%y, %H:%M')}})
                comment.save()
            else:
                result.update({'message':'Enter message please'})
        else:
            result.update({'message':'WOK.'})
    else:
        result.update({'message':'Login please'})
    return HttpResponse(simplejson.dumps(result), 'json')

def add_tag(request):
    result = {}
    if request.user:
        if request.is_ajax():
            bugurt = request.POST['bugurt']
            tag = request.POST['tag']
            if tag:
                bugurt_obj = Bugurt.objects.get(id=bugurt)
                tag_obj = Tag.objects.filter(title=tag)
                if bugurt_obj.author.username == request.user.username:
                    if tag_obj:
                        t = Tag.objects.get(title=tag)
                        btag = BugurtTags.objects.filter(bugurt=bugurt_obj, tag=tag_obj)
                        if not btag:
                            BugurtTags(bugurt=bugurt_obj, tag=t).save()
                            result.update({'tag': t.title, 'id': t.id})
                        else:
                            result.update({'message': 'Already exist'})
                    else:
                        t = Tag.objects.create(title=tag)
                        btag = BugurtTags.objects.filter(bugurt=bugurt_obj, tag=tag_obj)
                        if not btag:
                            BugurtTags(bugurt=bugurt_obj, tag=t).save()
                            result.update({'tag': t.title, 'id': t.id})
                        else:
                            result.update({'message': 'Already exist'})
                else:
                    result.update({'message':'4itak dohuya?'})
            else:
                result.update({'message':'Enter name tag please'})
        else:
            result.update({'message':'WOK.'})
    else:
        result.update({'message':'Login please'})
    return HttpResponse(simplejson.dumps(result), 'json')

def delete_tag(request):
    result = {}
    if request.user:
        if request.is_ajax():
            bugurt = request.POST['bugurt']
            tag = request.POST['tag']
            BugurtTags.objects.filter(bugurt=bugurt, tag=tag).delete()
            result.update({'bugurt': bugurt, 'tag': tag})
        else:
            result.update({'message':'WOK.'})
    else:
        result.update({'message':'Login please'})
    return HttpResponse(simplejson.dumps(result), 'json')

def add_proof(request):
    result = {}
    if request.user:
        if request.is_ajax():
            bugurt = request.POST['bugurt']
            proof = request.POST['proof']
            if proof:
                bugurt_obj = Bugurt.objects.get(id=bugurt)
                proof_obj = Proof.objects.filter(link=proof)
                if bugurt_obj.author.username == request.user.username:
                    if proof_obj:
                        p = Proof.objects.get(title=proof)
                        bproof = BugurtProofs.objects.filter(bugurt=bugurt_obj, proof=proof_obj)
                        if not bproof:
                            BugurtProofs(bugurt=bugurt_obj, proof=p).save()
                            result.update({'proof': p.link, 'id': p.id})
                        else:
                            result.update({'message': 'Already exist'})
                    else:
                        p = Proof.objects.create(link=proof)
                        bproof = BugurtProofs.objects.filter(bugurt=bugurt_obj, proof=proof_obj)
                        if not bproof:
                            BugurtProofs(bugurt=bugurt_obj, proof=p).save()
                            result.update({'proof': p.link, 'id': p.id})
                        else:
                            result.update({'message': 'Already exist'})
                else:
                    result.update({'message':'4itak dohuya?'})
            else:
                result.update({'message':'Enter name proof please'})
        else:
            result.update({'message':'WOK.'})
    else:
        result.update({'message':'Login please'})
    return HttpResponse(simplejson.dumps(result), 'json')

def delete_proof(request):
    result = {}
    if request.user:
        if request.is_ajax():
            bugurt = request.POST['bugurt']
            proof = request.POST['tag']
            BugurtProofs.objects.filter(bugurt=bugurt, proof=proof).delete()
            result.update({'bugurt': bugurt, 'proof': proof})
        else:
            result.update({'message':'WOK.'})
    else:
        result.update({'message':'Login please'})
    return HttpResponse(simplejson.dumps(result), 'json')
