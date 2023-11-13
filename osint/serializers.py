from rest_framework import serializers
from .models import *
from .utils import run_script_on_log

class RootSerializer(serializers.ModelSerializer):

    class Meta:
        model = Root
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'

class ChildSerializer(serializers.ModelSerializer):

    class Meta:
        model = Child
        fields = '__all__'

class ScriptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Script
        fields = '__all__'

class LogFileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Log
        fields = '__all__'

    def run_script(self, log_instance):
        script_instance = log_instance.parent_script
        print(script_instance)
        script_path = script_instance.get_script_path()
        print(script_path)
        log_file_path = os.path.join(settings.MEDIA_ROOT, str(log_instance.log_file))

        # Run the script on the log file and return the result
        # You'll need to implement the logic to run the script on the log file
        result = run_script_on_log(log_file_path, script_path)
        print('serializer', result)

        return result    