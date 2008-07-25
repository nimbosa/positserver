from django.conf.urls.defaults import *
#import positServer.posit.views as positViews
from  positServer.posit.views import *
import settings

urlpatterns = patterns('',
     (r'^$', home),
     (r'^posit/$', stats),
     (r'^images/$', images),	
     (r'^map/$', map),
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^app/$', appgen),
     (r'^app/2/$', appgen2),
     (r'^app/3/$', appgen3),
     (r'^app/4/$', strings),
     (r'^app/thanks/$', 'django.views.generic.simple.direct_to_template', {'template': 'thanks.html'}),
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^downloads/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.DOWNLOADS,
            'show_indexes': True,
        }),
     (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
     )
