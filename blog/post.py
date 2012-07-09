from blog.models import Post, Category, Comment

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response

import datetime
import time
import recaptcha.captcha as captcha

RECAPTCHA_PRV_KEY = "6LcpLcASAAAAAHdkv1eCIa9_zcpPf87AjQeM1pJo"
RECAPTCHA_PUB_KEY = "6LcpLcASAAAAAKTKws06izZyb0_MySa2BSLeAv6s"
POSTS_PER_PAGE = 999

MAX_COMMENT_NAME_LEN = 255
MAX_COMMENT_LEN = 2048 

# Last category is not displayed, 
# it holds the number of all post in all categories
# used for "Everything" category
def gen_category_list():
    try:
        cats = Category.objects.all()
        cat_count = list()
        c_sum = 0
        for cat in cats:
            count = len(Post.objects.filter(category=cat,draft=False))
            if (count > 0):
                cat_count.append([cat, count])
                c_sum += count
    except:
        cat_count = None

    cat_count.append([None, c_sum])
    return cat_count


def gen_comment_list(post_id):
    try:
        coms = Comment.objects.filter(post=post_id).filter(hide=0)
    except:
        coms = None

    return coms

def gen_post(post_id):
    try:
        p = Post.objects.get(id=post_id, draft=False)
    except:
        raise Http404

    cats = gen_category_list()
    comments = gen_comment_list(post_id)

    return {'post':p, 'cat_links':cats, 'com_list':comments, 'recapcha_pub_key':RECAPTCHA_PUB_KEY }


def page_indicies(len, cur_page):
    if (len < 1):
        return (0,0,0)

    pages_tot = (len / POSTS_PER_PAGE)

    if (cur_page < 1):
        cur_page = 1

    p_end = cur_page * POSTS_PER_PAGE
    p_start = p_end - POSTS_PER_PAGE

    if p_end > len:
        p_end = len
        if (pages_tot * POSTS_PER_PAGE) == len:
            p_start = (pages_tot-1) * POSTS_PER_PAGE
        else:
            p_start = (pages_tot * POSTS_PER_PAGE)

    if cur_page > pages_tot:
        cur_page = pages_tot

    if cur_page < 1:
        cur_page = 1

    return (p_start, p_end, cur_page)

"""
  Main index page
"""
def index(request, page=1):

    all_posts = Post.objects.filter(draft=False).order_by('-pub_date')

    (p_start, p_end, page) = page_indicies(len(all_posts), int(page))
                                     
    posts = all_posts[p_start:p_end]
        
    l_ar = "/index/" + str(page+1)
    r_ar = "/index/" + str(page-1)
    cats = gen_category_list()
        
    return render_to_response('index.html',
                              {'post_list':posts, 'cat_links':cats, 'l_ar':l_ar, 'r_ar':r_ar});

"""
  Post detail view
"""
def details(request, post_id):
    try:
        dict = gen_post(post_id)
    except:
        raise Http404

    return render_to_response('post.html', dict, context_instance=RequestContext(request))

 
"""
  Generate Category view
"""
def category(request, category_id, page=0):
    try:
        c = Category.objects.get(id=category_id)
    except:
       raise Http404
    
    all_posts = Post.objects.filter(category=c,draft=False).order_by('-pub_date')
    if len(all_posts) < 1:
        raise Http404

    (p_start, p_end, page) = page_indicies(len(all_posts), int(page))
                                     
    posts = all_posts[p_start:p_end]
        
    l_ar = "/category/" + str(category_id) + "/" + str(page+1)
    r_ar = "/category/" + str(category_id) + "/" + str(page-1)
    cats = gen_category_list()

    return render_to_response('index.html',
                              {'post_list':posts, 'cat_links':cats, 'l_ar':l_ar, 'r_ar':r_ar});


"""
  Process a comment
"""
def comment(request, post_id):

    # Try to get the post page
    try:
        page_dict = gen_post(post_id)
        if page_dict["post"].comments_enable == False:
            return HttpResponseRedirect('/post/'+post_id)
    except:
        raise Http404
    
    if request.method == 'POST':
        try:
            p = Post.objects.get(id=post_id)

            # Check the form captcha. If not good, pass the template an error code
            captcha_response = captcha.submit(
                request.POST.get("recaptcha_challenge_field", None),
                request.POST.get("recaptcha_response_field", None),
                RECAPTCHA_PRV_KEY,
                request.META.get("REMOTE_ADDR", None)
                )
            
            page_dict['comment_errors'] = ""

            if request.POST['name'] == "":
                page_dict['comment_errors'] += "Name can not be blank. "
            if len(request.POST['name']) > MAX_COMMENT_NAME_LEN:
                page_dict['comment_errors'] += "Name exceeds maximum length of "+str(MAX_COMMENT_NAME_LEN)+" characters. "
            if request.POST['body'] == "":
                page_dict['comment_errors'] += "Comment can not be blank. "
            if len(request.POST['body']) > MAX_COMMENT_LEN:
                page_dict['comment_errors'] += "Comment exceeds maximum length of "+str(MAX_COMMENT_LEN)+" characters. "
            if captcha_response.is_valid == False:
                page_dict['comment_errors'] +=  "Human verification failed. "

            if page_dict['comment_errors'] == "":
                name_fix = ''.join(ch for ch in request.POST['name'] if ch.isalnum())
                c = Comment(post=p,
                            name=name_fix,
                            body=request.POST['body'],
                            hide=False,
                            pub_date=datetime.datetime.fromtimestamp(time.time()-28800))
                c.save()
                return HttpResponseRedirect('/post/'+post_id+'/#'+str(c.pk))
            else:
                page_dict['comment_error_name'] = request.POST['name']
                page_dict['comment_error_body'] = request.POST['body']
                return render_to_response('post.html', page_dict, context_instance=RequestContext(request))
        except:
            raise Http404
        
    return HttpResponseRedirect('/post/'+post_id)
    
