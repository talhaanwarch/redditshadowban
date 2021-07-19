from django.forms import ModelForm
from .models import Text,FileModel
class TextForm(ModelForm):
	class Meta:
		model=Text
		fields=['username']

class FileForm(ModelForm):
	class Meta:
		model=FileModel
		fields=['filename','fileupload']
