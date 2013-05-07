
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


"""Urls for the Gstudio sitemap"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.ajaxviews',
                       url(r'^contentorgadd/$', 'AjaxAddContentOrg', name='ajax_views_contentorgadd'),
                       url(r'^ajaxcreatehtml/$', 'AjaxCreateHtml', name='ajax_views_createhtml'),
                       url(r'^ajaxcreatefile/$', 'AjaxCreateFile', name='ajax_views_createfile'),
                       url(r'^contentadd/$', 'AjaxAddContent', name='ajax_views_contentadd'),
                       )
