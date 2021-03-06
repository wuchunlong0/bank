#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse,redirect
from django.conf import settings
#from rbac.models import Permission

class RbacMiddleware(MiddlewareMixin):
    """用户权限信息校验"""
    
    def process_request(self, request):
        """当用户请求刚进入时候出发执行"""

        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表 
        3. 权限信息匹配
        """
        current_url = request.path_info  
        #print('current_url======', current_url)
        #print('settings.VALID_URL_LIST======', settings.VALID_URL_LIST)      
        for valid_url in settings.VALID_URL_LIST:
            #if valid_url == current_url:
            if re.match(valid_url, current_url):
                # 白名单中的URL无需权限验证即可访问
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return redirect('/login/?err=%s 无权限' %current_url)
            return HttpResponse('未获取到用户权限信息,请登录!')

        flag = False
        
        url_record = [
            {'title': '首页', 'url': '/'}
        ]
    
        for item in permission_dict.values():            
            reg = "^%s$" % item['url']
            if re.match(reg, current_url): 
                flag = True
                request.current_selected_permission = item['pid'] or item['id']
                if not item['pid']:
                    url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'},
                    ])
                request.breadcrumb = url_record
                break

        if not flag:
            return redirect('/login/?error=无权访问,请登录!')
            #return HttpResponse('无权访问')
         