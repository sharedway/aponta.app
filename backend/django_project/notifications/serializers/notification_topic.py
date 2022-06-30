
from rest_framework import serializers
from notifications.models import NotificationTopicModel

class NotificationTopicModelSerializer(serializers.ModelSerializer):   
    def create(self, validated_data):        
        criado_por = self.context.get('criado_por',None)
        if criado_por:
            validated_data.update({
                'criado_por':criado_por
            })
            
        instance = NotificationTopicModel.objects.create(**validated_data)       
        return instance

    class Meta:
        model = NotificationTopicModel
        fields = NotificationTopicModel.SERIALIZABLES
        if NotificationTopicModel.READ_ONLY_FIELDS:
            read_only_fields =NotificationTopicModel.READ_ONLY_FIELDS
