from rest_framework import mixins, viewsets
from Users.serializers import UserEducationSerializer
from Core.models import UserEducation

from rest_framework import status
from rest_framework.response import Response


class UserEducationLCUDView(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    
    """
    create:
    Aggiungi un tipo di educazione all'utente.
    
    Permette di aggiungere un tipo di educazione all'utente che ha fatto la richiesta.
    Puoi mandare una singola educazione oppure una lista di educazioni usando questo formato:
    [ { dati educazione }, { ... }, ... ]
    L'endponts non ritrona nessun valore.
    
    update:
    Aggiorna i dati di un tipo dell'educazione.
    
    Aggiorna i dati dell'educazione, l'educazione da aggiornare viene decisa in base all'id messo nell'url.
    Nel caso di un'aggiornamento parziale (PATCH) ritornano solo i campo aggiornati.
    
    partial_update:
    Aggiorna i dati di un tipo dell'educazione.
    
    Aggiorna i dati dell'educazione, l'educazione da aggiornare viene decisa in base all'id messo nell'url.
    Nel caso di un'aggiornamento parziale (PATCH) ritornano solo i campo aggiornati.
    
    destroy:
    Rimuovi un tipo dell'educazione da un utente.
    
    Rimuovi un tipo dell'educazione da un utente, l'educazione da eliminare viene decisa in base all'id messo nell'url.
    """
    serializer_class = UserEducationSerializer
    queryset = UserEducation.objects.all()
    lookup_field = "id"
    
    def get_queryset(self):
        return UserEducation.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return super(UserEducationLCUDView, self).create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        response = super().update(request,*args,**kwargs)
        if response.status_code != 200: return response
        return Response(data=request.data,
                        status=response.status_code,
                        headers=response.headers)