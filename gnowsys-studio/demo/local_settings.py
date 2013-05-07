

DATABASES = {
    'default':
             {'ENGINE': 'django.db.backends.sqlite3',
              'NAME': os.path.join(os.path.dirname(__file__), 'demo.db')}
             } ,

    'new':
        {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'metastudio_production',
        'USER':'glab',
        'PASSWORD':'aiglab2homah',
        'HOST':'localhost',
        'PORT':'5432',
    }
