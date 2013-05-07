
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
from django.template import RequestContext
from django.shortcuts import render_to_response


import json
import shutil
from gstudio.models import *
from tagging.models import Tag, TaggedItem
from objectapp.models import *
rlist={}
import os
from settings import PYSCRIPT_URL_GSTUDIO

def AjaxGetSchemaTP(request):
	counter=0
	counter1=0
	counter2=0
	
	json="{"
	if request.method =="GET":
		pg_id = request.GET['data']
	elif request.method =="POST":
		pg_id = request.POST#['curr_page']
	else:
		print 'Error no request variable'
	
	pg_obj = Gbobject.objects.get(id = pg_id)
	print 'title : ',pg_obj.title
	json += '"name":"' + pg_obj.title + '",\n'
	json += '"degree" : 1,\n'
	json += '"children":\n\t[\n'
	print 'json content before tags : ',json
	
	#title_obj = Gbobject.objects.get(title = pg_obj.title)
	tag_arr = Tag.objects.get_for_object(pg_obj)
		
	if tag_arr:
		for tag in tag_arr:
			if counter1 >0:
				json +=",\n"
			json += '\t\t{"name":"' + tag.name + '","degree" : 2 ,\n\t\t"children":\n\t\t[\n'
			queryset = TaggedItem.objects.get_by_model(Gbobject.published.all(), tag)
			
			counter2 = 0
			for obj in queryset:
			    
				if counter2 > 0:
					json +=",\n"
				counter = 0	
				t = Tag.objects.get_for_object(obj)
				for rows in t:
					counter +=1
				c = str(counter)
				url = 'http://beta.metastudio.org' + obj.get_view_object_url
			    	
			    	json += '\t\t\t{"name":"'+ str(obj.title) + '","url":"'+ url + '","page_id":'+ str(obj.id) + ',"size" : "' + c + '"}'
		    		counter2 += 1
		    	counter1 += 1				
			json += '\t\t]}'	
			
	json+="]}"
	return HttpResponse(json)
	

def AjaxAttribute(request):
    iden = request.GET["id"]
    attr = Attributetype.objects.get(id=iden)
    subjecttype = attr.subjecttype
    returndict = {}

    for ots in Objecttype.objects.all():
        if attr.subjecttype.id ==ots.id:
            for member in ots.get_members:
                returndict[member.id] = member.title
            childrenots = ots.get_children()
        
            if childrenots:
                for eachchild in childrenots:
                    returndict[eachchild.id] = eachchild.title    
                    membs=eachchild.ref.get_members
                    for each in membs:
                        returndict[each.id] = each.title

    jsonobject = json.dumps(returndict)
    return HttpResponse(jsonobject, "application/json")

def AjaxRelationleft(request):
    global rlist
    rlist={}
    idenid=request.GET["id"]
    rts=Relationtype.objects.filter(id=idenid)
    for each in rts:
        subj=str(each.left_subjecttype.title)
        appltype=each.left_applicable_nodetypes
        fnname= "selectionlist_"+appltype+"('"+subj+"')" 
        
        exec fnname
    
    returndict=rlist  
    jsonobject = json.dumps(returndict)
    return HttpResponse(jsonobject, "application/json") 

def AjaxRelationright(request):
    global rlist
    rlist={}
    idenid = request.GET["id"]
    rts=Relationtype.objects.filter(id=idenid)
    print "rtsright",rts
    for each in rts:
       subj=str(each.right_subjecttype.title)
       appltype=each.right_applicable_nodetypes
       fnname="selectionlist_"+appltype+"('"+subj+"')"
       
       exec fnname
    
    returndict=rlist
    jsonobject = json.dumps(returndict)
    return HttpResponse(jsonobject, "application/json") 
                
def additemdict(sdict,itemtoadd):
    fl=0
    for key,value in sdict.items():
        if value==itemtoadd:
            fl=1
    if fl==0:
        sdict[itemtoadd.id]=itemtoadd.title
    return sdict                 
def selectionlist_OT(obj):
    # Basically the filter must filter out the OT, their members, the children and members of the children

    global rlist
    # Return all OTs and members of subtypes of OT
    obs=Objecttype.objects.filter(title=obj)
    #	Get all members of subtypes of each OT
    if obs: 
        # Add the items first
        for each in obs:
            rlist=additemdict(rlist,each)
        obs=Objecttype.objects.get(title=obj)
        # Add the objects first
        # for each in obs:
        #     rlist = additemdict(rlist,each)
        memobs=obs.get_members
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        # Add children first
        for each in childrenots:
            rlist=additemdict(rlist,each)
        # Add memebers of each child
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)


        
    return rlist 
            
def selectionlist_MT(obj):
    global rlist
    # Return all MTs and members of subtypes of MT
    obs=Metatype.objects.filter(title=obj)
    #Get all members of subtypes of each MT
    if obs:
    	obs=Metatype.objects.get(title=obj)
	memobs=obs.member_types.all()
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
               childrenots=each.ref.get_members
               if childrenots:
    		   for eachchild in childrenots:
        	        rlist=additemdict(rlist,eachchild)
      
    return rlist
def selectionlist_NT(obj):
    global rlist
    # Return all NTs and members of subtypes of NT
    obs=Nodetype.objects.filter(title=obj)
    #Get all members of subtypes of each NT
    if obs: 
        obs=Nodetype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist
def selectionlist_AT(obj):
    global rlist
    # Return all ATs and members of subtypes of AT
    obs=Attributetype.objects.filter(title=obj)
    #Get all members of subtypes of each AT
    if obs:
        obs=Attributetype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist
def selectionlist_ST(obj):
    global rlist
    # Return all STs and members of subtypes of ST
    obs=Systemtype.objects.filter(title=obj)
    #Get all members of subtypes of each ST
    if obs:
        obs=Systemtype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist
def selectionlist_PT(obj):
    global rlist
    # Return all PTs and members of subtypes of PT
    obs=Processtype.objects.filter(title=obj)
    #Get all members of subtypes of each PT
    if obs:
        obs=Processtype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist
def selectionlist_RT(obj):
    global rlist
    # Return all RTs and members of subtypes of RT
    obs=Relationtype.objects.filter(title=obj)
    #Get all members of subtypes of each RT
    if obs:
        obs=Relationtype.objects.get(title=obj)
        memobs=obs.get_members
        
        if memobs:
            for each in memobs:
               rlist=additemdict(rlist,each)
        childrenots=obs.get_children()
        
        if childrenots:
            for eachchild in childrenots: 
                membs=eachchild.ref.get_members
                for each in membs:
                    rlist=additemdict(rlist,each)
    return rlist

def selectionlist_RN(obj):
    global rlist
    
    obs=Relation.objects.filter(title=obj)
    #Get all members of RN
    if obs:
        obs=Relation.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist

def selectionlist_AS(obj):
    global rlist
    
    obs=AttributeSpecification.objects.filter(title=obj)
    #Get all members of AS
    if obs:
        obs=AttributeSpecification.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_NS(obj):
    global rlist
    
    obs=NodeSpecification.objects.filter(title=obj)
    #Get all members of NS
    if obs:
        obs=NodeSpecification.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_SY(obj):
    global rlist
    
    obs=System.objects.filter(title=obj)
    #Get all members of SY
    if obs:
        obs=System.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_RS(obj):
    global rlist
    # Return all members of RS
    obs=RelationSpecification.objects.filter(title=obj)
    if obs:
        obs=RelationSpecification.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist

def selectionlist_ND(obj):
    global rlist
    
    obs=Node.objects.filter(title=obj)
    #Get all members of ND
    if obs:
        obs=Node.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_ED(obj):
    global rlist
    
    obs=Edge.objects.filter(title=obj)
    #Get all members of ED
    if obs:
        obs=Edge.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist
def selectionlist_IN(obj):
    global rlist
    
    obs=Intersection.objects.filter(title=obj)
    #Get all members of IN
    if obs:
        obs=Intersection.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist

def selectionlist_CP(obj):
    global rlist
    
    obs=Complement.objects.filter(title=obj)
    #Get all members of CP
    if obs:
        obs=Complement.objects.get(title=obj)
        rlist=additemdict(rlist,obs)
    return rlist

def selectionlist_UP(obj):
    global rlist
    
    obs=Objecttype.objects.all()
    #Get all members UP
    print 'obs=',obs
    for each in obs:
        childrenots=each.get_children()
        for eachchild in childrenots: 
            membs=eachchild.objecttypes.all()
def selectionlist_OB(obj):
    global rlist
    obs=Objecttype.objects.get(title=obj)
    #Get all members of OB
    for each in  obs.member_objects.all(): 
        rlist=additemdict(rlist,each)
    return rlist
    
def AjaxAddContentOrg(request):
    iden = request.GET["id"]
    content = request.GET["contentorg"]
    nid = NID.objects.get(id = iden)
    refobj = nid.ref
    refobj.content_org = content
    refobj.save()
    return HttpResponse("sucess")


def AjaxCreateFile(request):
    usr=str(request.user)
    iden = request.GET["id"]
    orgcontent = request.GET["content_org"]
    ext='.org'
    html='.html'
    myfile = open(os.path.join('/tmp/',usr+ext),'w')
    myfile.write(new_ob.content_org)
    myfile.close()
    myfile = open(os.path.join('/tmp/',usr+ext),'r')
    myfile.readline()
    myfile = open(os.path.join('/tmp/',usr+ext),'a')
    myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
    myfile.write("\n#+TITLE: ")
    myfile = open(os.path.join('/tmp/',usr+ext),'r')
    return HttpResponse("test sucess")

def AjaxCreateHtml(request):
    usr=str(request.user)
    ext='.org'
    stdout = os.popen("%s %s"%(PYSCRIPT_URL_GSTUDIO,usr+ext))
    output = stdout.read()
    return HttpResponse("sucess")

def AjaxAddContent(request):
    usr=str(request.user)
    html='.html'
    iden = request.GET["id"]
    nid = NID.objects.get(id = iden)
    refobj = nid.ref
    data = open(os.path.join('/tmp/',usr+html))
    data1 = data.readlines()
    data2 = data1[72:]
    data3 = data2[:-3]
    newdata=""
    for line in data3:
        newdata += line.lstrip()
    refobj.content= newdata
    refobj.save()
    return HttpResponse(refobj.content)


def AjaxAddDrawer(request):
    list1=request.GET["title"]
    wtitle=request.GET["wtitle"]
    list1=list1+","
    list2=eval(list1)
    sys=System.objects.get(title=wtitle)
    sys.gbobject_set.clear()
    i=0
    n_set=[]

    
    while i<len(list2):
        objs=Gbobject.objects.get(title=list2[i])
      
        sys.gbobject_set.add(objs)
        n_set.append(list2[i])
        i=i+1
    var=sys.in_gbobject_set_of.__dict__['through']
    varobset=[]
    for each in var.objects.all():
        print sys.id,sys.title,each.system_id
        if each.system_id == sys.id:
            s=Gbobject.objects.get(id=each.gbobject_id)
            s1=s.title
            varobset.append(s)
    
    variables = RequestContext(request, {'sys':sys,'list':n_set,'objset':varobset})
    template = "metadashboard/newcollection.html"
    
    return render_to_response(template, variables)
def HtmlExport(request):
    ptitle=request.GET["ptitle"]
    set1=request.GET["title"]
    set1=set1+","
    set2=eval(set1)

    ptitle=System.objects.get(title=ptitle)
    contorg=ptitle.content_org    #ptitle=eval(ptitle)
    content_org="* "+str(ptitle)+"\n"+contorg.encode('utf8')
    set2=[]
    set2=ptitle.gbobject_set.all()
    l=len(set2)
    i=0
    if l>0:
        while i<len(set2):
            st=System.objects.get(title=set2[i])
            stcontorg=st.content_org
            content_org += "** "+str(set2[i])+"\n"+stcontorg.encode('utf8')+"\n"
                
            if st.gbobject_set.exists():
                gbset=st.gbobject_set.all()
                
                for each in gbset:
                    subst=System.objects.get(title=each)
                    
                    content_org += "*** "+str(each)+"\n"+each.content_org.encode('utf8')+"\n"
                    if subst.gbobject_set.exists():
                        subgbset=subst.gbobject_set.all()
                        for each in subgbset:
                            subtwost=System.objects.get(title=each)
      
                            content_org += "**** "+str(each)+"\n"+each.content_org.encode('utf8')+"\n"
                        
                            if subtwost.gbobject_set.exists():
                                subtwogbset=subtwost.gbobject_set.all()
                                for each in subtwogbset:
                                    content_org += "***** "+str(each)+"\n"+each.content_org.encode('utf8')+"\n"
                    
            i+=1
            
   
    s=ptitle.get_ssid.pop()
    fname=str(s)+"-download"
    ext=".org"
    myfile = open(os.path.join(FILE_URL,fname+ext),'w')
    myfile.write(content_org)
    myfile.close()
    myfile = open(os.path.join(FILE_URL,fname+ext),'a')
    myfile.write("\n#+OPTIONS: timestamp:nil author:nil creator:nil  H:3 num:nil toc:nil @:t ::t |:t ^:t -:t f:t *:t <:t")
    myfile.write("\n#+TITLE: ")
    myfile = open(os.path.join(FILE_URL,fname+ext),'r')
    stdout = os.popen("%s %s %s"%(PYSCRIPT_URL_GSTUDIO,fname+ext,FILE_URL))
    output = stdout.read()
    file1= fname+".html"
    print file1
    src=FILE_URL+fname+".html"
    des=HTML_FILE_URL
    file_relocate=shutil.copy(src,des)
    fname1=fname+".html"
    print "tttt"
    print fname1 
    variables = RequestContext(request, {'fname':fname1,'newfname':"test"})
    template = "metadashboard/newdownload.html"
    return render_to_response(template, variables)

    

def AjaxAddCollection(request):
    title1=request.GET["title"]
    collection=request.GET["collection"]
    uid=request.GET["uid"]
    usr=request.GET["usr"]
    orgcontent=request.GET["orgcontent"]
    list1=request.GET["list"]
    list1=list1.split(",");
    create_wikipage(title1,uid,orgcontent,usr,collection,list1)
    return HttpResponseRedirect("/gstudio/page/gnowsys-page/1815")

def IsWiki(request):
    ptitle=request.GET["title"]
    iswiki=Gbobject.objects.filter(title=ptitle)
    if iswiki:
        return HttpResponse("sucess")
	
                    
                
                

            



	
	
	
	
