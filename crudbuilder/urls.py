
from django.conf.urls import url
from django.db import connection

import crudbuilder
from crudbuilder.views import ViewBuilder
from crudbuilder import helpers
helpers.auto_discover()

urlpatterns = []

tables = connection.introspection.table_names()

if tables:
    for app_model, base_crud in crudbuilder.registry.items():
        app, model = app_model.split('-')
        viewbuilder = ViewBuilder(app, model, base_crud)

        urls = []
        pluralized = helpers.plural(model)

        list_view = viewbuilder.generate_list_view()
        update_view = viewbuilder.generate_update_view()
        detail_view = viewbuilder.generate_detail_view()
        create_view = viewbuilder.generate_create_view()
        delete_view = viewbuilder.generate_delete_view()

        entries = [
            (r'^{}/{}/$', list_view.as_view(), '{}-{}-list'),
            (r'^{}/{}/(?P<pk>\d+)/$', detail_view.as_view(), '{}-{}-detail'),
            (r'^{}/{}/create/$', create_view.as_view(), '{}-{}-create'),
            (r'^{}/{}/(?P<pk>\d+)/update/$',
                update_view.as_view(),
                '{}-{}-update'),
            (r'^{}/{}/(?P<pk>\d+)/delete/$',
                delete_view.as_view(),
                '{}-{}-delete'),
            ]

        for entry in entries:
            address = entry[0].format(app, pluralized)
            url_name = entry[2].format(app, model)

            urls.append(
                url(address, entry[1], name=url_name),
            )
        urlpatterns += urls
