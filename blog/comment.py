from blog.models import Post, Category, Comment
import datetime
import recaptcha.captcha as captcha

from django.http import HttpResponse, Http404
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

def form(request, post_id):
    try:
        p = Post.objects.get(id=post_id)
        c = Comment.objects.filter(post=p)
    except:
        c = None
    return render_to_response('comments.html', {'post_id' : post_id, 'com_list' : c},
                              context_instance=RequestContext(request))

def make(request, post_id):
    try:

        p = Post.objects.get(id=post_id)
        c = Comment(post=p,
                    name=request.POST['name'],
                    body=request.POST['body'],
                    pub_date=datetime.datetime.now())
        c.save()
        return HttpResponse("OK")
    except Post.DoesNotExist:
        return HttpResponse("ERROR")
    

def make(request):
    return HttpResponse("OK")
