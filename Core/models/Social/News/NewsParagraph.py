from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractName, News
import uuid

class NewsParagraph(AbstractName):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    news = models.ForeignKey(News,
                             on_delete=models.CASCADE,
                             related_name="paragraphes",
                             related_query_name="peragraphes")
    order_paragraph = models.IntegerField(_("order paragraph"),default=0)
    content = models.TextField(_("content"))
    
    class Meta:
        db_table = "news_paragraph"
        verbose_name = _("News Paragraph")
        verbose_name_plural = _("News Paragraphes")