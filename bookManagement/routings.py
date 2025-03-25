from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import events.channels.routing # type: ignore
import api.reservations.routing # type: ignore
import api.events.routing # type: ignore
application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            events.channels.routing.websocket_urlpatterns  + api.events.routing.websocket_urlpatterns + api.reservations.routing.websocket_urlpatterns
        )
    ),
})