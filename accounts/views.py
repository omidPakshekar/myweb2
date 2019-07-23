from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.http import JsonResponse
from common.decorators import ajax_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Contact
from actions.utils import create_action
from actions.models import Actions

# if user is following others, retrive only their Actions
# every time you retrive the action object you probally acess is
# related user object and probally acess user related profile object too
# django orm offers the simple way to retrive related object once
# select_related is used to retrive one to many relationsheep
# select_related is used for foreign key and one to one fileds
# it works by performin sql join
# we use user_profile to join profile table to one single sql query if you called select_related without passing any arguments it retrive object from all foreign key in relationship
# select_related can not work for many to many ,many to one relationship
# and django provide prefetch_related for many to many and many to one relationship
#  prefetch_related is also for genericforeignkey and genericrelationship

@login_required
def dashboard(request):
    # Display all actions by default
    actions = Actions.objects.all().exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
    actions = actions[:10]

    return render(request, 'accounts/dashboard.html', {'section': 'dashboard',
                                                      'actions': actions})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # set chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)

            create_action(new_user, 'has created an accounts')

        return render(request,
        'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form':user_form})


@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,
        							data=request.POST)

		profile_form = ProfileEditForm(instance=request.user.profile,
											data=request.POST,
											files = request.FILES)

		if user_form.is_valid() and profile_form.is_valid():
		    user_form.save()
		    profile_form.save()
		    messages.success(request, 'Profile update successfully')
		else:
			messages.error (request, 'Error updating your profile')
	else:
	    user_form = UserEditForm(instance=request.user)
	    profile_form=ProfileEditForm(instance=request.user.profile)

	return render(request, 'accounts/edit.html',
	    	{'user_form': user_form, 'profile_form':profile_form})

@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'accounts/user/detail.html', {'section': 'people','user': user})

@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'accounts/user/list.html', {'section': 'people',
                                                        'users': users})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'ko'})
    return JsonResponse({'status':'ko'})
