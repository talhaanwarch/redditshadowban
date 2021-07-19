from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Text(models.Model):
	username=models.CharField(max_length=200)

	def __str__(self):
		return self.username

class FileModel(models.Model):
	filename=models.CharField(max_length=200)
	fileupload=models.FileField(upload_to='media',
		validators=[FileExtensionValidator(allowed_extensions=['txt'])])
	def __str__(self):
		return self.filename