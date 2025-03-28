from django.urls import path, include
from api.configuration.routers import urlpatterns as router_config 
from api.transaction.routers import urlpatterns as router_transaction

urlpatterns = []
urlpatterns += router_config
urlpatterns += router_transaction
    # path("app/",include(ConfigurationRouter.urls)),
    # path("app/news/", include(NewsRouter.urls)),
    # path("app/pages/",include(PagesRouter.urls)),
    # path("app/services/",include(service_router)),
    # path("app/assistan/",include(AssistantRouter.urls)),
