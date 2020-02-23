# -*- coding: UTF-8 -*-
import os
import django
import shutil

def syncdb():
    
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    django.setup()

    from rbac.models import UserInfo
    #shutil.copyfile("db.sqlite3", "db_db.sqlite3")  
    
    #给数据库写入数据 这里设想是给db_db.sqlite3写入新数据, 实际是给db.sqlite3写入数据了
    items = [('root_100','123','a@1.com','CEO'), ('root1_100','123','b@1.com','主管'), 
               ('root2_100','123','c@1.com','普通用户'), ('赵力全_100','123','d@1.com','普通用户')]
    items = [UserInfo(name=i[0], password =i[1], email=i[2]) for i in items]
    UserInfo.objects.bulk_create(items, batch_size=20) 

#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
#     django.setup()
#     
#     # 文件改名
#     os.rename("db_db.sqlite3", "db.sqlite3")
     
if __name__ == "__main__":
    syncdb()
    print('Done!')