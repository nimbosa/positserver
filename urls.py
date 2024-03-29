from django.conf.urls.defaults import *
#import positServer.posit.views as positViews
from  positServer.posit.views import * #ok, I admit I'm lazy
from positServer.posit.xmlrpc import *
from django.contrib import admin

import settings
admin.autodiscover()


urlpatterns = patterns('',
     (r'^$', home),
     (r'^stats/$', stats),
     (r'^images/$', images),	
     (r'^map/$', map),
     (r'^accounts/',include('registration.urls')),
     (r'^app/$', appgen),
     (r'^app/2/$', appgen2),
     (r'^app/3/$', appgen3),
     (r'^app/4/$', strings),
     (r'^app/final/$', appgenfinal),
     (r'^dl/$', downloads),
     (r'^app/thanks/$', 'django.views.generic.simple.direct_to_template', {'template': 'thanks.html'}),
     (r'^downloads/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.DOWNLOADS,
            'show_indexes': True,
        }),
     (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
     (r'^xml_rpc/', rpc_handler), #getting it from positServer.posit.xmlrpc
     (r'^admin/(.*)', admin.site.root),
     (r'^profile/',include('profiles.urls')),
     )
