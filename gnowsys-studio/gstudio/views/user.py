# Copyright (c) 2011,  2012 Free Software Foundation

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.



from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gstudio.methods import *

def userdashboard(request):#,username):
	# if request.user.username == username :
	print "loom"
    	meetings = Systemtype.objects.get(title="Meeting")
        variables = RequestContext(request,{"meetings" : meetings })
    	template = "metadashboard/userdashboard.html"
    	return render_to_response(template, variables)
    #else :
     #    variables = RequestContext(request)
      #   template = "metadashboard/logindashboard.html"
       #  return render_to_response(template,variables)

def wikidashboard(request):#,username):
    #if request.user.username == username :
    	pages = Systemtype.objects.get(title="Wikipage")
        variables = RequestContext(request,{"pages" : pages })
    	template = "metadashboard/wikidashboard.html"
    	return render_to_response(template, variables)
    #else :
     #    variables = RequestContext(request)
      #   template = "metadashboard/logindashboard.html"
       #  return render_to_response(template,variables)

    


    
