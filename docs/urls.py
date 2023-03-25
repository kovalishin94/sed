from django.urls import path
from django.conf.urls.static import static
from sed.settings import MEDIA_ROOT, MEDIA_URL, DEBUG
from .views import *


urlpatterns = [
    path('', index, name='auth'),
    path('logout/', user_logout, name='logout'),
    path('outbox/', ListOutbox.as_view(), name='outbox'),
    path('agree/', ListAgree.as_view(), name='agree'),
    path('newoutbox/', CreateOutbox.as_view(), name='newoutbox'),
    path('deldoc/<int:pk>', del_doc, name='deldoc'),
    path('agree/<int:pk>', agree, name='agree'),
    path('revision/<int:pk>', revision, name='revision'),
    path('updateoutbox/<int:pk>', UpdateOutbox.as_view(), name='updateoutbox'),
    path('ajax/', ajax, name='ajax'),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
