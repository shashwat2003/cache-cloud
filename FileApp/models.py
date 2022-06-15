from django.db import models
from UserApp.models import User
from FolderApp.models import Folder
# Create your models here.
def get_user_directory(instance, filename):
        return 'user_{0}/folder_{1}/'.format(instance.folder.user.id, instance.folder.id)

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to=get_user_directory)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    accessed_at = models.DateTimeField(null=True)
    

