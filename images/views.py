from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from common.decorators import ajax_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from actions.utils import create_action
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)
@login_required
def image_create(requset):
	"""
	View for createing an image using the javascript Bookmarklet
	"""
	if requset.method == 'POST':
		# form is sent
		form = ImageCreateForm(data=requset.POST)
		if form.is_valid():
			# form data is valid
			cd = form.cleaned_data
			new_item = form.save(commit=False)
			# assign current user to the item
			new_item.user = requset.user
			new_item.save()
			create_action(requset.user, 'bookmarked image', new_item)
			messages.success(requset, 'Image added successfully')
			# redirect to new created item detail view
			return redirect(new_item.get_absolute_url())
	else:
		# build form with data provided by the bookmarklet via GET
		form = ImageCreateForm(data=requset.GET)

	return render(requset, 'images/image/create.html', {'section': 'images','form' : form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1. the incr method return the value of key after performed
	# we create redis key with notaion like objectType:id:fields we use clone for seperate keys
    total_views = r.incr('image:{}:views'.format(image.id))
    # increment image ranking by 1 redisSortSet a sorted set is non reapiting collection of string
	# which every member assosiate with score. item sorted by score
    r.zincrby('image_ranking', image.id, 1)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image,
                   'total_views': total_views})

# decorator is a function that thake another function and extense the behavir
@ajax_required
@login_required
@require_POST
def image_like(request):
	image_id = request.POST.get('id')
	action = request.POST.get('action')
	if image_id and action:
		try:
			image = Image.objects.get(id=image_id)
			if action == 'like':
				image.users_like.add(request.user)
				create_action(request.user, 'likes', image)
			else:
				image.users_like.remove(request.user)
			return JsonResponse({'status': 'ok'})
		except:
			pass
	return JsonResponse({'status':'ko'})

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                   {'section': 'images', 'images': images})



@login_required
def image_ranking(request):
	# get image ranking dictionary, we use zrange to obtain sorted set this command expect custom range
	# with lowest and highst score by zero az lowest and -1 to highest scroe
	# desc = True is retrive item by order the sending score
	image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
	image_ranking_ids = [int(id) for id in image_ranking]
	# get most viewed images
	most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))

	most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
	return render(request,
	              'images/image/ranking.html',
	              {'section': 'images',
	               'most_viewed': most_viewed})
