from django import forms
from .models import Image

from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify

# we don't use imageurl directory in the form instead we want 
# to use a java script tools to choose image from a external site
# and we recive a url as a parameters
class ImageCreateForm(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('title', 'url', 'description')
		# we override the default widget of url field
		# to use hidden input this widget render as html input element
		# with hidden input
		widget= {
			'url': forms.HiddenInput, 
		}

	def clean_url(self):
		url = self.cleaned_data['url']
		valid_extensions = ['jpg', 'jpeg']
		extension = url.rsplit('.', 1)[1].lower()
		if extension not in valid_extensions:
			raise forms.ValidationError('The given url does not match valid image extension')

		return url
	#  in addition to validating to given url we also need 
	# download image file and save it we could use views to download image file
	# instead we are gone take general aporach by overriding saving method 
	def save(self, force_insert=False, force_update=False, commit=True):
		image = super(ImageCreateForm, self).save(commit=False )
		image_url = self.cleaned_data['url']
		image_name = '{}.{}'.format(slugify(image.title),
									image_url.rsplit('.',1)[1].lower())
		# download image from given url with python lib
		response = request.urlopen(image_url)
		# we set save to false to avoid saving object
		image.image.save(image_name,
						ContentFile(response.read()),
						save=False) 
		if commit:
			image.save()
		else:
			return image
