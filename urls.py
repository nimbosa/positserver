from django.conf.urls.defaults import *
#import positServer.posit.views as positViews
from  positServer.posit.views import home, images, stats, map
import settings

urlpatterns = patterns('',
     (r'^$', home),
     (r'^posit/$', stats),
     (r'^images/$', images),	
     (r'^map/$', map),
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
)
