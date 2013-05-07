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
from django.shortcuts import render_to_response
from django.template import RequestContext
from demo.settings import *
from gstudio.models import *
from tagging.models import Tag, TaggedItem
from objectapp.models import *
import os
from gstudio.methods import *
from PIL import Image
import glob, os
import hashlib
from django.template.defaultfilters import slugify
from django.template.loader import get_template
from django.template import Context

size = 128, 128
report = "true"
md5_checksum = ""
def image(request):
	p=Objecttype.objects.get(title="Image")
	q=p.get_nbh['contains_members']
	if request.method=="POST":
		title = request.POST.get("title1","")
		content= unicode(request.POST.get("contenttext",""))
		simg = request.POST.get("simg","")
		sub3 = request.POST.get("mydropdown","")
		user = request.POST.get("user","")
		delete = request.POST.get("delete","")
		rating = request.POST.get("star1","")
		imgid = request.POST.get("imgid","")
		pict = request.POST.get("pict","")
		fulid = request.POST.get("fulid","")
		show = request.POST.get("Show","")
		addtags = request.POST.get("addtags","")
		texttags = unicode(request.POST.get("texttags",""))
		contenttext = request.POST.get("contenttext","")
		fav=request.POST.get("fav","")
		if show != "":
			i=Gbobject.objects.get(id=fulid)
			vars=RequestContext(request,{'image':i})
			template="gstudio/fullscreen.html"
			return render_to_response(template, vars)

		if fav != "" :
			list1=[]
			t=Gbobject.objects.filter(title=user+"image")
			if t:
			    t=Gbobject.objects.get(title=user+"image")
			    if t.get_relations():
				    for each in t.get_nbh['has_favourite']:
					    d=each.right_subject_id
					    x=Gbobject.objects.get(id=d)
					    list1.append(x)
			variables = RequestContext(request,{'images':list1,'fav':fav})
			template = "gstudio/image.html"
			return render_to_response(template, variables)	
		
		
		if rating :
        	 	rate_it(int(imgid),request,int(rating))
		if delete != "":
			each=q.get(id=pict)
			each.delete()
			ti=each.title
			os.system("rm -f "+MEDIA_ROOTNEW+'/'+ti)
			p=Objecttype.objects.get(title="Image")
			q=p.get_nbh['contains_members']
			vars=RequestContext(request,{'images':q,'val':simg})
			template="gstudio/image.html"
			return render_to_response(template, vars)
		if sub3 != "":
			if simg != "":
				vidon = Objecttype.objects.get(title="Image")
				vido_new = vidon.get_nbh['contains_members']
				vido = vido_new.filter(title__contains=simg)
				vido2 = vido.order_by(sub3)
				variables = RequestContext(request,{'images':vido2,'val':simg})
				template = "gstudio/image.html"
				return render_to_response(template, variables)
			else:
				vidon = Objecttype.objects.get(title="Image")
				vido_new = vidon.get_nbh['contains_members']
				vido=vido_new.order_by(sub3)
				variables = RequestContext(request,{'images':vido,'val':simg})
				template = "gstudio/image.html"
				return render_to_response(template, variables)


		if addtags != "":
			i=Gbobject.objects.get(id=imgid)
			i.tags = i.tags+ ","+(texttags)
			i.save()

		
		a=[]
		reportid=''
		for each in request.FILES.getlist("image[]",""):
			a.append(each)
		if a != "":
			i=0
			for f in a:
				if i==0:
					report,imageeachid = save_file(f,title,user)
					if report == "false":
						reportid = imageeachid
					else:
						create_object(f,user,title,content,str(request.user))
						i=i+1
				else:	
					report,imageeachid = save_file(f,title+'_'+str(i),user)
					if report == "false":
						reportid = imageeachid
					else:
						create_object(f,user,title+'_'+str(i),content,str(request.user))
						i=i+1
			p=Objecttype.objects.get(title="Image")
			q=p.get_nbh['contains_members']
			vars=RequestContext(request,{'images':q,'reportid':reportid,'report':report})
			template="gstudio/image.html"
			return render_to_response(template, vars)	
	vars=RequestContext(request,{'images':q,'val':""})
	template="gstudio/image.html"
	return render_to_response(template, vars)

def save_file(file,title, user, path=""):
        report = "true"
	imageeachid = ''
	filename = title
	slugfile = str(file)
	slugfile=slugfile.replace(' ','_')
	os.system("mkdir -p "+ MEDIA_ROOTNEW2+"/"+user)
    	fd = open('%s/%s/%s' % (MEDIA_ROOTNEW2, str(user),str(path) + str(slugfile)), 'wb')
    	for chunk in file.chunks():
        	fd.write(chunk)
    		fd.close()
	global md5_checksum
	md5_checksum = md5Checksum(MEDIA_ROOTNEW2+"/"+ str(user)+"/"+slugfile)
	attype = Attributetype.objects.get(title="md5_checksum_image")
	att = Attribute.objects.all()
	flag = 0
	for each in att:
		if each.attributetype.id == attype.id:
			if each.svalue == md5_checksum :
				flag = 1
				imageeachid = each.subject.id
	if flag == 1:
		report = "false"
	else:	
		for infile in glob.glob(MEDIA_ROOTNEW2+"/"+str(user)+"/"+str(slugfile)):
			file, ext = os.path.splitext(infile)
			im = Image.open(infile)
			imm = Image.open(infile)
			im.thumbnail(size, Image.ANTIALIAS)
			im.save(file + "-thumbnail", "JPEG")
			width, height = imm.size
			sizem = 1024,height
			if int(width) > 1024:
				imm.thumbnail(sizem, Image.ANTIALIAS)
				imm.save(file + "_display_1024","JPEG")
			else:
				imm.thumbnail(imm.size,Image.ANTIALIAS)
				imm.save(file + "_display_1024","JPEG")
    	return report,imageeachid	


def create_object(f,log,title,content,usr):
	p=Gbobject()
	filename = str(f)
	filename=filename.replace(' ','_')
	p.title=title
        fname=slugify(title)+"-"+usr
	p.image=log+"/"+filename
	#final = ''
	#for each1 in filename:
	#	if each1==" ":
	#		final=final+'-'
	#	else:
	#		final = final+each1	
	#i=0
	#dirname = ""
	#while final[i] != ".":
	#	dirname = dirname + final[i]
	#	i=i+1
	p.slug=slugify(p.title)
	contorg=unicode(content)
	p.content_org=contorg.encode('utf8')
	p.status=2
	p.save()
	p.slug = p.slug + "-" + str(p.id)
	p.sites.add(Site.objects.get_current())
	p.save()
	s=Author.objects.get(username=log)
	p.authors.add(s)
	p.save()
	q=Objecttype.objects.get(title="Image")
	p.objecttypes.add(Objecttype.objects.get(id=q.id))
	p.save()
	new_ob = content
 	ext='.org'
        html='.html'
 	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(p.content_org)
	myfile.close()
	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
        rfile=myfile.readlines()
	scontent="".join(rfile)
	newcontent=scontent.replace("\r","")
	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(newcontent)
	#myfile.readline()
	myfile = open(os.path.join(FILE_URL,fname+ext),'a')
	myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
	myfile.write("\n#+TITLE: ")
	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
	stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
	output = stdout.read()
	data = open(os.path.join(FILE_URL,fname+html))
 	data1 = data.readlines()
 	data2 = data1[107:]
        dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'

 	data3 = data2[:-6]
 	newdata=""
 	for line in data3:
        	newdata += line.lstrip()
 	p.content = newdata
 	p.save()
        a=Attribute()
        a.attributetype=Attributetype.objects.get(title="md5_checksum_image")
        a.subject=p
        a.svalue=md5_checksum
        a.save()


def rate_it(topic_id,request,rating):
	ob = Gbobject.objects.get(id=topic_id)
	ob.rating.add(score=rating ,user=request.user, ip_address=request.META['REMOTE_ADDR'])
	return True

def show(request,imageid):
	if request.method=="POST":
		rating = request.POST.get("star1","")
		imgid = request.POST.get("imgid","")
		addtags = request.POST.get("addtags","")
		texttags = unicode(request.POST.get("texttags",""))
		contenttext = unicode(request.POST.get("contenttext",""))
		favid=request.POST.get("favid","")
		favusr=request.POST.get("favusr","")
		removefavid = request.POST.get("removefavid","")
		titlecontenttext = request.POST.get("titlecontenttext","")
		if rating :
	       	 	rate_it(int(imgid),request,int(rating))
		if addtags != "":
			i=Gbobject.objects.get(id=imgid)
			i.tags = i.tags+ ","+(texttags)
			i.save()
		if contenttext !="":
			 edit_description(imgid,contenttext,str(request.user))

		if favid!="":
                        e=0
                        r = Objecttype.objects.get(title="user")
                        for each in r.get_nbh['contains_members']:
                                if favusr+"image" == each.title:
                                    e=1
                        if e==0 :
				t=Gbobject()
                                t.title=favusr+"image"
                                t.slug=favusr+"image"
                                t.content=' '
                                t.status=2
                                t.save()
                                t.objecttypes.add(Objecttype.objects.get(title="user"))
                                t.save()
                        t=Gbobject.objects.get(title=favusr+"image")
                        rel=Relation()
                        rt=Relationtype.objects.get(title="has_favourite")
                        rel.relationtype_id=rt.id
                        f1=Gbobject.objects.get(id=favid)
                        rel.left_subject_id=t.id
                        rel.right_subject_id=f1.id
                        rel.save()
			t.save()
		if removefavid !="":
			objects = Gbobject.objects.get(id=removefavid)
			objects.get_relations()['is_favourite_of'][0].delete()
		if titlecontenttext !="":
			new_ob = Gbobject.objects.get(id=int(imgid))
			new_ob.title = titlecontenttext
			new_ob.save()

	gbobject = Gbobject.objects.get(id=imageid)
	relation = ""
	if gbobject.get_relations():
		if gbobject.get_relations()['is_favourite_of']:
			rel = gbobject.get_relations()['is_favourite_of'][0]
			print rel
			reluser = rel._left_subject_cache.title
			if str(reluser) == str(request.user)+str("image"):
				relation = "rel"
	vars=RequestContext(request,{'image':gbobject,'relation':relation})
	template="gstudio/fullscreen.html"
	return render_to_response(template,vars)

def edit_description(sec_id,title,usr):
	new_ob = Gbobject.objects.get(id=int(sec_id))
	contorg=unicode(title)
	ssid=new_ob.get_ssid.pop()
	fname=str(ssid)+"-"+usr
	new_ob.content_org=contorg.encode('utf8')
	ext='.org'
	html='.html'
	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(new_ob.content_org)
	myfile.close()
	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
	rfile=myfile.readlines()
	scontent="".join(rfile)
	newcontent=scontent.replace("\r","")
	myfile = open(os.path.join(FILE_URL,fname+ext),'w')
	myfile.write(newcontent)
	#myfile.readline()
	myfile = open(os.path.join(FILE_URL,fname+ext),'a')
	myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
	myfile.write("\n#+TITLE: ")
	myfile = open(os.path.join(FILE_URL,fname+ext),'r')
	stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
	
	output = stdout.read()
	data = open(os.path.join(FILE_URL,fname+html))
	data1 = data.readlines()
	data2 = data1[107:]
        dataa = data2[data2.index('<div id="content">\n')]='<div id=" "\n'

	data3 = data2[:-6]
	newdata=""
	for line in data3:
		newdata += line.lstrip()
	new_ob.content = newdata
	new_ob.save()
	return True

def md5Checksum(filePath):
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


def edit_title(request):
	nidtitle = ""
	if request.method =="GET":
		print "iin get "
		title=request.GET['title']
		titleid=request.GET['titleid']
		nid=NID.objects.get(id=titleid)
		nid.title=title
		nid.save()
		nid=NID.objects.get(id=titleid)
		nidtitle = nid.title
  	t = get_template('gstudio/editedobjecttitle.html')
	html = t.render(Context({'title':nidtitle}))
	return HttpResponse(html)


def addpriorpost(request):
	titleid=""
	gbid1=""
	if request.method =="GET":
		print "in get"
		title=request.GET['title']
		titleid=request.GET['titleid']
		gbid1=Gbobject.objects.get(id=titleid)
		gbid2 = Gbobject.objects.get(title=title)
		gbid1.prior_nodes.add(gbid2)
		gbid1.save()
		gbid2.posterior_nodes.add(gbid1)
		gbid2.save()
		gbid1=Gbobject.objects.get(id=titleid)
	priorgbobject = gbid1.prior_nodes.all()
	posteriorgbobject = gbid1.posterior_nodes.all()
  	t = get_template('gstudio/repriorpost.html')
	html = t.render(Context({'priorgbobject':priorgbobject,'posteriorgbobject':posteriorgbobject,'objectid':titleid,'optionpriorpost':"priorpost"}))
	return HttpResponse(html)
	#return HttpResponseRedirect("/gstudio/resources/images/")

def addtag(request):
	i= ""
	if request.method =="GET":
		objectid=request.GET['objectid']
		data=request.GET['data']
		i=Gbobject.objects.get(id=objectid)
		i.tags = i.tags+ ","+(data)
		i.save()
		i=Gbobject.objects.get(id=objectid)
		
  	t = get_template('gstudio/repriorpost.html')
	html = t.render(RequestContext(request,{'viewtag':i,'optiontag':"tag","objectid":objectid}))
	return HttpResponse(html)

def deletetag(request):
	i= ""
	objectid=""
	if request.method =="GET":
		objectid=request.GET['objectid']
		data=request.GET['data']
		i=Gbobject.objects.get(id=objectid)
		delval = i.tags.replace(data+",","")
		delval1 = delval.replace(data,"")
		i.tags = delval1
		i.save()
		i=Gbobject.objects.get(id=objectid)
  	t = get_template('gstudio/repriorpost.html')
	html = t.render(RequestContext(request,{'viewtag':i,'optiontag':"tag","objectid":objectid}))
	return HttpResponse(html)

def get_pgtitle(request):
	
	counter=0
	json=""
	if request.method =="GET":
		t_id=request.GET['data']
		
		tag = Tag.objects.get(id = t_id)
		queryset = TaggedItem.objects.get_by_model(Gbobject.published.all(), tag)
		
		if queryset:
			json="["
			for obj in queryset:
				print 'Object : ',obj
				if counter>0:
					json+=","
				
				json +='{"page_title":"' + str(obj.title) + '","page_id":'+ str(obj.id) + '}'
				counter +=1		
			json+="]"
			
	json+=""
  	return HttpResponse(json)
	
def get_url(request):
	if request.method =="GET":
		page_id=request.GET['data']
	obj = Gbobject.objects.get(id=page_id)
	#url = '{"url": http://beta.metastudio.org' + obj.get_view_object_url + '}'
	url = 'http://beta.metastudio.org' + obj.get_view_object_url
	return HttpResponse(url)

def tagclouds_data(request):
	#node = NID.objects.filter(nodemodel="Gbobject")
	tag = Tag.objects.all()
        str_data = "[\n"
        
	if tag:
		#f = open(FILE_URL1,'w')
		
		flag = 0
		
		for t in tag:
			
			if flag:
				str_data += ',\n'
			flag = 1
			
			tag_name = t.name
			str_data += '\t{\n\t\t"tag_name": "'+ str(tag_name) + '",\n'
			str_data += '\t\t"tag_id":' + str(t.id) +',\n'
			str_data += '\t\t"pages" : [\n\t\t\t\t\t'

			queryset = TaggedItem.objects.get_by_model(Gbobject.published.all(), t)
			
			counter = 0
			for obj1 in queryset:
			    
			    if counter > 0:
				str_data +=",\n\t\t\t\t\t"
			    str_data += '{"page_title" : "'+ str(obj1.title) + '"'
			    			    
			    #retreving associated tags with current object obj1
			    
			    #tag_arr = Tag.objects.get_for_object(obj1) 
			    #str_data += ',"associated_tags" : ['
			    #t_counter = 0
			    #for t in tag_arr:
			    #    if t_counter > 0:
			    #	     str_data += ","

			    #	t_counter += 1
			    #	str_data += '{"tag" : "'+ str(t.name) +'"}'
			    #str_data  += ']'
			    str_data += '}'
			    counter += 1

			c = str(counter)				
			str_data += '\n\t\t\t\t  ],\n\t\t"weight" : "' + c + '"\n'
			str_data += '\t}'
			
			
		str_data += "\n]"	
		#f.write(str_data)	
	
		#f.close()
	
	#JSON file for fetching URL and TITLE
	
	#	f = open(FILE_URL2,'w')	
	#	obj = Gbobject.objects.all()
	#	str_data2 = '['
	#	for ob in obj:
	#		url = "beta.metastudio.org" + ob.get_view_object_url #+ "/"
	#		title = ob.title
#
#			str_data2 += '\t\t{"page_title" : "' + ob.title + '","url" : "' + str(url) + '"}\n'
#		
#		str_data2 += ']'
#		f.write(str_data2)	
#		f.close()
	
	else: 
		return HttpResponse('No tag available, Can\'t create file')
	return HttpResponse(str_data)

def tagclouds(request):
		
	t = get_template('gstudio/WordTagcloud.html')
	html = t.render(RequestContext(request,{}))
	return HttpResponse(html)
	


