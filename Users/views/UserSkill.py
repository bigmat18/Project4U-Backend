from rest_framework import viewsets, mixins
from Core.models import UserSkill
from Users.serializers import UserSkillCreateSerializer

from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

create_responses = {"201": openapi.Response(description="In caso di aggiunta di una o più skill riuscita",
                                            schema=openapi.Schema(type=openapi.TYPE_OBJECT,properties={})),
                    "400": openapi.Response(description="Nel caso in cui sia stata aggiunta una skilla da presente per quello user",
                                            schema=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
                                                "skill":openapi.Schema(type=openapi.TYPE_STRING)}),
                                            examples={"application/json":{"skill":"è già stata abbinata questa skill a questo utente"}}),
                    "400.": openapi.Response(description="Caso in cui l'id della skill mandato non fa riferito a nessuna skill esistente",
                                            schema=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
                                                "error":openapi.Schema(type=openapi.TYPE_STRING)}),
                                            examples={"application/json":{"Error":"è già stata abbinata questa skill a questo utente"}})}

class UserSkillCUDView(mixins.CreateModelMixin,mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    create:
    Aggiungi una skill all'utente
    
    Permette di aggiungere una skill con il livello all'utente a cui è riferito lo slug nell'url.
    Puoi mandare una singola skill oppure una lista di skills usando questo formato:
    [ { dati skill }, { ... }, ... ]
        
    update:
    Aggiorna i dati di una skill  
    
    Aggiorna i dati della skill, la skill da aggiornare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
      
    destroy:
    Rimuovi una skill da un utente
    
    Rimuovi una skill da un utente, la skill da eliminare viene decisa in base all'id della skill messo nell'url ({skill} = id skill)
    """
    serializer_class = UserSkillCreateSerializer
    queryset = UserSkill.objects.all()
    lookup_field = "skill"
    
    def get_queryset(self):
        skill = self.kwargs.get("skill")
        return UserSkill.objects.filter(skill=skill).filter(user=self.request.user)
    
    @swagger_auto_schema(responses=create_responses,request_body=UserSkillCreateSerializer(many=True))
    def create(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            response = super(UserSkillCUDView, self).create(request, *args, **kwargs)
            response.data = {}
            return response
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        try: serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"error":"è già stata abbinata questa skill a questo utente"})