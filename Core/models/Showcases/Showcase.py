from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractName, Project, AbstractText
from django.conf import settings
import uuid


class Showcase(AbstractName, AbstractText):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="showcases",
                                related_query_name="showcases")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="showcases",
                                   related_query_name="showcases",
                                   blank=True)
    class Meta:
        db_table = "showcase"
        verbose_name = _("Showcase")
        verbose_name_plural = _("Showcases")
