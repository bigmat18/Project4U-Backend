from rest_framework import serializers
from Core.models import Event, EventTask, User

class EventPartecipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "image", "slug"]


class EventTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventTask
        fields = ["checked", "name", "id"]


class EventReadSerializer(serializers.ModelSerializer):
    tasks = EventTaskSerializer(many=True, read_only=True)
    partecipants = EventPartecipantsSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ["id","started_at","ended_at","description",
                  "partecipants","tasks","image", "name"]
        
      
class EventWriteSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Event
        fields = ["started_at","ended_at","description",
                  "partecipants","id", "updated_at","image", "name"]
        