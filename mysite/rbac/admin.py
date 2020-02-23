# -*- coding: UTF-8 -*-
import os
from django.contrib import admin
from .models import UserInfo, Role, Permission, Menu 
from django.conf.urls import url, include
from django.http.response import HttpResponseRedirect
from django.conf import settings

STATEFILE = os.path.join(settings.BASE_DIR, 'statefile.txt') # 状态文件
 

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

    """ admin 添加按钮
        一、关于访问后台admin数据库问题：
        1、在此写入代码后，首次访问页面时，是执行后台代码的，以后再访问该页面，就不执行后台代码了。
        访问页面 http://localhost:8000/admin/classroom/course/
        2、添加按钮，后台数据如何传到前端？
        
        二、本例采用另外方法，实现下列功能：
        1、admin 添加按钮
        2、按‘数据库状态’按钮，判断statefile.txt 状态文件是否存在
        如果状态文件不存在(允许更新同步)，显示‘数据库状态’按钮、‘同步数据库’按钮。按‘同步数据库’按钮，创建一个状态文件
        如果状态文件存在(正在同步中)，显示‘数据库状态’按钮、‘数据库同步中，请稍等...’。 
        
        三、admin 后台实现更新数据库数据
        1、 用命令不能更新数据(本机运行正常，部署后不能更新数据)，原因不清楚？
        2、本实例用函数实现， admin后台实现更新数据库数据，成功！
        3、更新数据库数据的逻辑：
        （1）创建状态文件
        （2）更新数据库数据
        （3）删除状态文件
          
    """
    
    change_list_template = "entities/sync-in-progress.html"     
    def get_urls(self):        
        urls = super().get_urls()
        my_urls = [
            url('sync_in_progress/', self.sync_in_progress),
            url('allow_sync/', self.allow_sync),
        ]
        return my_urls + urls
    
    def sync_in_progress(self, request):
        """ 同步数据库(正在同步中) """
        self.change_list_template = "entities/sync-in-progress.html"  
               
        #from rbac.views.user import syncdb 
        #from syncdb import syncdb           
        if request.method == 'POST':
            with open(STATEFILE,'w+') as fp:  
                fp.write('0') 
                                            
            #meg = syncdb()  # 更新数据库数据 ok
            
            # 用命令不能更新数据(本机运行正常，部署后不能更新数据)，原因不清楚？
            cmdStr = (r'python syncdb.py')   
            meg = os.system(cmdStr) # 返回值错误代码：https://blog.csdn.net/CrazyUncle/article/details/84565966
            meg = '正常' if meg == 256 else '异常代码：%s' %meg
                
                              
            if os.path.isfile(STATEFILE): #判断文件
                os.remove(STATEFILE)                                         
            self.message_user(request, '%s 同步完成.' %meg) 
            self.change_list_template = "entities/allow-sync.html"             
        return HttpResponseRedirect("../")
     
    def allow_sync(self, request):
        """判断文件是否存在"""        
        if os.path.exists(STATEFILE):
            # 状态文件存在 正在同步... 此时是不能更新数据库数据
            self.change_list_template = "entities/sync-in-progress.html"             
        else:
            # 状态文件不存在,显示‘数据库状态’按钮, 允许更新数据库数据
            self.change_list_template = "entities/allow-sync.html" 
        return HttpResponseRedirect("../")

    
        
    ''' admin add button
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
        #print('===='+os.getcwd()) #当前目录
        
        # 用命令不能更新数据(本机运行正常，部署后不能更新数据)，原因不清楚？
        # cmdStr = (r'python syncdb.py')   
        # os.system(cmdStr)
        
        from rbac.views.user import syncdb    
        meg = syncdb()
        self.message_user(request, meg) 
        return HttpResponseRedirect("../") 
    '''
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):   
    list_display = ('id', 'title', 'permissions_list')
    def permissions_list(self, role):
        """自定义列表字段"""
        return [u.title for u in role.permissions.all()]

@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):    
    list_display = ('id', 'title', 'url', 'name','menu','pid')

