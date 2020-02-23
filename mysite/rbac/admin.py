# -*- coding: UTF-8 -*-
import os
from django.contrib import admin
from .models import UserInfo, Role, Permission, Menu 
from django.conf.urls import url, include
from django.http.response import HttpResponseRedirect
    
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):    
    list_display = ('id', 'title', 'icon', )


@admin.register(UserInfo)    
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'password', 'email', 'role_list')
    def role_list(self, userInfo):
        """自定义列表字段"""
        return [u.title for u in userInfo.roles.all()]
    
    list_display_links = ('name',)
    search_fields = ('name','password', 'email',)
    
        
    """admin add button"""
    change_list_template = "entities/heroes_changelist.html"       
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url('immortal/', self.set_immortal),
        ]
        return my_urls + urls
    def set_immortal(self, request):
        """后台在这里加代码"""
        #self.message_user(request, "All heroes are now mortal")
        print('===='+os.getcwd()) #当前目录
        meg = "update ok"
        try:
            #cmdStr = (r'python syncdb.py')   
            #os.system(cmdStr)
            from rbac.models import UserInfo    
            #给数据库写入数据 
            items = [('root_100','123','a@1.com','CEO'), ('root1_100','123','b@1.com','主管'), 
               ('root2_100','123','c@1.com','普通用户'), ('赵力全_100','123','d@1.com','普通用户')]
            items = [UserInfo(name=i[0], password =i[1], email=i[2]) for i in items]
            UserInfo.objects.bulk_create(items, batch_size=20) 
            
        except Exception as ex:
            meg = 'err: %s' %ex
            print('err: %s' %ex) 
        self.message_user(request, meg) 
        return HttpResponseRedirect("../") 
           
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):   
    list_display = ('id', 'title', 'permissions_list')
    def permissions_list(self, role):
        """自定义列表字段"""
        return [u.title for u in role.permissions.all()]

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):    
    list_display = ('id', 'title', 'url', 'name','menu','pid')

