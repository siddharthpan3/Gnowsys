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



"""Url for Gstudio User Dashboard"""
from django.conf.urls.defaults import url
from django.conf.urls.defaults import patterns

urlpatterns = patterns('gstudio.views.group',
                       url(r'^notify/([_\w]+)/(\d+)/(\d+)/$','notifyactivity',name='notify'),
			url(r'^notify/(\d+)/(\d+)/$','notifyuser',name='group_notify'),
			url(r'^notify/unsubscribe/(\d+)/(\d+)/$','notifyuserunsubscribe',name='group_notify_unsubscribe'),
                       url(r'^gnowsys-grp/(\d+)/$', 'groupdashboard', name='gstudio_group'),
                     url(r'^later$', 'grouplater', name='gstudio_group'),
                      url(r'^over$', 'groupover',
                           name='gstudio_group'),
                       )
