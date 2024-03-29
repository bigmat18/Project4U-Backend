from random import choice, choices
from Core.models import Message, Showcase, TextMessage, MessageFile
from rest_framework import generics, viewsets
from ..serializers import MessageSerializer, TextMessageSerializer, MessageFileSerializer
import django_filters as filters
from rest_access_policy import AccessPolicy
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from Core.models.Projects.Message import TypeMessage


class MessagePagintation(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'size'


class MessageAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list", "create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_showcase"
        },
    ]
    
    def is_inside_showcase(self, request, view, action) -> bool:
        showcase = view.get_showcase()
        return (request.user == showcase.creator or 
                showcase.users.filter(id=request.user.id).exists())


class MessageFilter(filters.FilterSet):
    gt_updated_at = filters.DateTimeFilter(method='get_gt_updated_at')
    type_message = filters.ChoiceFilter(method="get_type_message",
                                        choices=TypeMessage.choices)
    
    class Meta:
        model = Message
        fields = ["type_message", "gt_updated_at"]
        
    def get_gt_updated_at(self, queryset, name, value):
        return queryset.filter(updated_at__gt=value)
    
    def get_type_message(self, queryset, name, value):
        return queryset.filter(type_message__in=dict(self.data)['type_message'])
    

class MessageListView(generics.ListAPIView,
                      viewsets.GenericViewSet):
    """
    list:
    Restituisce la lista dei messaggi.
    
    Restituisce una lista con tutti i messaggi della bacheca di cui è stato passato l'id.
    E' possibile filtrare i tipi di messaggi scrivendo nell'url '?type_message=' ed accanto il tipo di messaggio
    fra TEXT, IDEA, EVENT, UPDATE, POLL, si possono invaire anche più tipi per filtrare scrivendo '?type_message=...&type_message=...' ed al posto di ... la stringa. 
    La lista che ritorna ritorna in ordine dall'utlimo messaggio scritto inoltre è organizzata in pagine da 25. Per cambiare pagina '?page=', per cambiare dimensioni pagine '?size='.
    E' possibile filtrare tutti i messagi in modo che vengano restituiti solato quelli con una data seguente a quella inviata nell'url tramite '?gt_updated_at='. 
    La data deve essere formattata con il formato in cui viene inviato nelle response del backend.
    Ogni volta che si richiede la lista delle pagine tutti i messaggi in quella pagina vengono segnati come visualizzati dall'utente
    che ha effetuato la richiesta. Soltato i partecipanti alla bacheca possono vedere la lista dei messaggi.
    
    -----IMPORTANTE----
    Il campo 'content' non è una stringa ma restituisce un oggetto con i capi del messaggio, vedi in fondo
    alla pagina TextMessage, EventRead, ShowocaseUpdate, PollRead modelli per vedere i campi.
    """
    serializer_class = MessageSerializer
    filterset_class = MessageFilter
    pagination_class = MessagePagintation
    permission_classes = [IsAuthenticated, MessageAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)

    def get_showcase(self):
        if hasattr(self, "showcase"): return self.showcase
        self.showcase = Showcase.objects.filter(id=self.kwargs['id'])\
                                        .select_related("creator")\
                                        .prefetch_related('users')\
                                        .first()
        return self.showcase
    
    def get_queryset(self):
        return Message.objects.filter(showcase=self.get_showcase())\
                              .select_related('text_message','event','showcase_update','poll',"author")\
                              .order_by("-updated_at")
                              
    def set_message_visualize(self, messages):
        for message in messages:
            message.viewed_by.add(self.request.user)
                              
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            self.set_message_visualize(page)
            serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)




class TextMessageCreateView(generics.CreateAPIView,
                            viewsets.GenericViewSet):
    """
    create:
    Create un messaggio testuale.
    
    Crea un nuovo messaggio testuale nella bacheca di cui è stato passato l'id.
    Soltato i partecipanti alla bacheca possono creare un messaggio.
    Il creatore del messaggio viene già aggiunto fra quelli che hanno visualizzato il messaggio.
    """
    serializer_class = TextMessageSerializer
    permission_classes = [IsAuthenticated, MessageAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_showcase(self):
        if hasattr(self, "showcase"): return self.showcase
        self.showcase = Showcase.objects.filter(id=self.kwargs['id'])\
                                        .select_related("creator")\
                                        .prefetch_related('users')\
                                        .first()
        return self.showcase
    
    def perform_create(self, serializer):
        instance = serializer.save(showcase=self.get_showcase(),
                                   type_message="TEXT",
                                   author=self.request.user)
        instance.viewed_by.add(self.request.user)
        
        
        
class MessageFileCreateView(generics.CreateAPIView,
                            viewsets.GenericViewSet):
    serializer_class = MessageFileSerializer
    
    def get_object(self):
        return get_object_or_404(TextMessage, id=self.kwargs['id'])
    
    def create(self, request, *args, **kwargs):
        if len(dict(request.data)['file']) > 1:
            response = []
            for file in dict(request.data)['file']:
                file = MessageFile.objects.create(message=self.get_object(),file=file)
                response.append(str(file.file))
            return Response(response, status=status.HTTP_201_CREATED)
        else: return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(message=self.get_object())