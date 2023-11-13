from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from .permissions import IsAdminOrStaff
from .utils import run_script_on_log

class RootListView(generics.ListAPIView):
    queryset = Root.objects.all()
    serializer_class = RootSerializer

class RootRetrieveView(generics.RetrieveAPIView):
    queryset = Root.objects.all()
    serializer_class = RootSerializer

    def retrieve(self, request, pk):
        try:
            root = Root.objects.get(id=pk)
            children = Folder.objects.filter(parent_root=root)
            serializer = FolderSerializer(children, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Root.DoesNotExist:
            return Response({"detail": "Root not found."}, status=status.HTTP_404_NOT_FOUND)        
        

class FolderListView(generics.ListAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

class FolderRetrieveView(generics.RetrieveAPIView):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer

    def retrieve(self, request, pk):
        try:
            folder = Folder.objects.get(id=pk)
            children = Folder.objects.filter(parent_folder=folder)
            child_children = Child.objects.filter(parent_folder=folder)
            folder_serializer = FolderSerializer(children, many=True)
            child_serializer = ChildSerializer(child_children, many=True)
            result_serializer = folder_serializer.data + child_serializer.data
            return Response(result_serializer, status=status.HTTP_200_OK)
        except Folder.DoesNotExist:
            return Response({"detail": "Folder not found."}, status=status.HTTP_404_NOT_FOUND)  

class ChildListView(generics.ListAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

class ChildRetrieveView(generics.RetrieveAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

    def retrieve(self, request, pk):
        try:
            child = Child.objects.get(id=pk)
            children = Script.objects.filter(parent_child=child)
            serializer = ScriptSerializer(children, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Child.DoesNotExist:
            return Response({"detail": "Child not found."}, status=status.HTTP_404_NOT_FOUND)  


class ScriptViewSet(viewsets.ModelViewSet):
    queryset = Script.objects.all()
    serializer_class = ScriptSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['update', 'create', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdminOrStaff()]
        return super().get_permissions()

class LogFileUploadView(generics.ListCreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogFileUploadSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Run the script on the uploaded log file
        result = serializer.run_script(serializer.instance)

        headers = self.get_success_headers(serializer.data)
        return Response({"result": result}, status=status.HTTP_201_CREATED, headers=headers)
    
    # def perform_create(self, request, *args, **kwargs):
    #     serializer = LogFileUploadSerializer(data=request.data)
    #     if serializer.is_valid():
    #         script_id = serializer.validated_data['script_id']
    #         log_file = serializer.validated_data['log_file']
    #         try:
    #             script = Script.objects.get(pk=script_id)
    #             script_path = script.get_script_path()
    #             result = run_script_on_log(log_file, script_path)
    #             return Response({'result': result}, status=status.HTTP_200_OK)
    #         except Script.DoesNotExist:
    #             return Response({'error': 'Script not found.'}, status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                