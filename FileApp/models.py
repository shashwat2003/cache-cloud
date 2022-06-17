from django.db import models
from UserApp.models import User
from FolderApp.models import Folder
# Create your models here.
def get_user_directory(instance, filename):
        return 'user_{0}/folder_{1}/{2}'.format(instance.folder.user.id, instance.folder.id, filename)
class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_user_directory)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    accessed_at = models.DateTimeField(null=True)
    catogery = models.ForeignKey('Catogery',on_delete=models.DO_NOTHING)
    filename = models.CharField(max_length=300, default=None, null=True)
    size = models.CharField(max_length=20,default=None, null=True)

class Catogery(models.Model):
    name = models.CharField(max_length=50)
    size = models.BigIntegerField()

class MiMeType(models.Model):
    catogery = models.ForeignKey(Catogery, on_delete=models.CASCADE)
    type = models.CharField(max_length=125, primary_key=True)
