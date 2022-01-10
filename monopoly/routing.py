from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'join/(?P<host_name>[@+-\.\w]+)/(?P<map_id>[-\w]+)', consumers.JoinConsumer.as_asgi()),
    re_path(r'game/(?P<host_name>[@+-\.\w]+)/(?P<mode>.*)', consumers.GameConsumer.as_asgi()),
    re_path(r'game/(?P<host_name>[@+-\.\w]+)', consumers.GameConsumer.as_asgi()),

]