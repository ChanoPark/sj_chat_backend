DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'sj_chat',
        'USER' : 'daisy',
        'PASSWORD' : '1q2w3e4r!',
        'HOST' : 'sj-chat-backend-mysql.cgdjipqmvxyp.ap-northeast-2.rds.amazonaws.com',
        'PORT' : '3306',
        'OPTION': {
            'init_command': 'SET sql_mode="STRICT_TRANS_TABLES"'
        }

    }
}

SECRET_KEY = '-1+!lkv@yiax5$$_2wg1i__v9!(i=esw#uqh@+*5%_th_s9v0('