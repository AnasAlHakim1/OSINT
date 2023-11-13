from django.db import models
from django.conf import settings
import os
from .utils import *

class Root(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    
class Folder(models.Model):
    parent_root = models.ForeignKey(Root, blank=True, null=True, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        parent_folders_string = get_parent_folders_as_string_with_root(self)
        return f"{self.name} in {parent_folders_string}"

    
class Child(models.Model):
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    steps = models.TextField(max_length=2500)
    link = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='child/', blank=True, null=True)

    def __str__(self):
        parent_folders_string = get_parent_folders_as_string(self)
        return f"{self.name} in {parent_folders_string}"

class Script(models.Model):
    parent_child = models.ForeignKey(Child, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    python_script = models.FileField(upload_to="scripts/")

    def get_parent_hierarchy(self):
        parent_folders_string = get_parent_folders_as_string(self.parent_child)
        return parent_folders_string

    def __str__(self):
        parent_hierarchy = self.get_parent_hierarchy()
        return f"{self.name} in {parent_hierarchy}\{self.parent_child.name}"
    
    def get_script_path(self):
        return os.path.join(settings.MEDIA_ROOT, str(self.python_script))

class Log(models.Model):
    parent_script = models.ForeignKey(Script, on_delete=models.CASCADE)
    log_file = models.FileField(upload_to="logs/")

    def __str__(self):
        return f"log for {self.parent_script.name}"             