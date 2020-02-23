# -*- coding: UTF-8 -*-
import os
from .models import UserInfo

def syncdb(): 
    try:               
        
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
        django.setup()
        
        #给数据库写入数据 
        items = [('root_100','1234','a@1.com','CEO'), ('root1_100','123','b@1.com','主管'), 
                ('root2_100','123','c@1.com','普通用户'), ('赵力全_100','123','d@1.com','普通用户')]
        items = [UserInfo(name=i[0], password =i[1], email=i[2]) for i in items]
        UserInfo.objects.bulk_create(items, batch_size=20)
        meg = "%s Record update complete" %len(items) 
        print('给数据库写入数据=========')
    except Exception as ex:
        meg = 'err: %s' %ex
        print('meg=========', meg)
    return  meg


if __name__=='__main__':     
    syncdb()