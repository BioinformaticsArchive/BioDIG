'''
	Application for the Images Page of the DOME
	URL: /images
	
	Author: Andrew Oberlin
	Date: July 23, 2012
'''
from taxon_home.models import Picture
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.core.servers.basehttp import FileWrapper
import os

'''
	Adds a prefix check on user permissions before serving media files
'''
def renderAction(request, *args, **kwargs):
	authorized = False
	query = request.path_info.split('media/')[1]
	filename = os.path.join(settings.MEDIA_ROOT, query)
	# check for thumbnail
	thumbnailCheck = query.split('thumbnails/')
	if len(thumbnailCheck) > 1:
		query = os.path.join('pictures', thumbnailCheck[1])
	if request.user and request.user.is_authenticated():
		if request.user.is_staff:
			authorized = True
		else:
			authorized = Picture.objects.get(imageName=query).readPermissions(request.user)
	else:
		try:
			authorized = not Picture.objects.get(imageName=query).isPrivate
		except Exception:
			return HttpResponseNotFound()
	
	if authorized:
		try:
			response = HttpResponse(FileWrapper(file(filename)), mimetype="image/png")
			response['Content-Length'] = os.path.getsize(filename)
			return response
		except Exception:
			return HttpResponseNotFound()
	else:
		return HttpResponseNotFound()