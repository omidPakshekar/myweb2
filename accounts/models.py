from django.db import models

from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	date_of_birth = models.DateField(blank=True, null=True)
	# we are install pillow to manage image in python
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

	def __str__(self):
		return 'profile for uesr {}'.format(self.user.username)

class Contact(models.Model):
	# related_name return a query set for a contact model
	user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
	user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True, db_index=True)
	# in order to acsess inside of the relationshep from the user model is hard to show many to many relationshep
	class Meta:
		ordering = ('-created',)

	def __str__(self):
		return '{} follows {}'.format(self.user_form, self.user_to)

# add following field to User dynamically
# add_to_class is not good way to add field in the field
# symmetrical=False it mean's if you follow me it does'nt mean i'm follow you
User.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))
