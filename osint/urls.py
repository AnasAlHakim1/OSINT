from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

ScriptRouter = DefaultRouter()
ScriptRouter.register('', ScriptViewSet, basename='ScriptViewSet')

urlpatterns = [
    path("root/", RootListView.as_view(), name= 'root-list'),
    path("root/<int:pk>/", RootRetrieveView.as_view(), name= 'root-retrieve'),
    path("folder/", FolderListView.as_view(), name= 'folder-list'),
    path("folder/<int:pk>/", FolderRetrieveView.as_view(), name= 'folder-retrieve'),
    path("child/", ChildListView.as_view(), name= 'child-list'),
    path("child/<int:pk>/", ChildRetrieveView.as_view(), name= 'child-retrieve'),        
    path("script/", include(ScriptRouter.urls)),
    path('upload-log/', LogFileUploadView.as_view(), name='upload_log'),
]