from django.urls import path
from django.conf.urls.static import static
from sed.settings import MEDIA_ROOT, MEDIA_URL, DEBUG
from .views import *


urlpatterns = [
    path('', index, name='auth'),
    path('logout/', user_logout, name='logout'),
    path('main/', main, name='main'),
    path('newoutbox/', newoutbox, name='newoutbox'),
    path('deldoc/<int:pk>', del_doc, name='deldoc'),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
