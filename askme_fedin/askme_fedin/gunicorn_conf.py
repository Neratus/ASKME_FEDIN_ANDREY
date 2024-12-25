# askme_fedin/gunicorn_conf.py

import multiprocessing

bind = "127.0.0.1:8000"
workers =  2 + 1
accesslog = '/Users/ekaterinafedina/ASKME_FEDIN_ANDREY/askme_fedin/askme_fedin/askme_fedin.gunicorn.tag'
errorlog = '/Users/ekaterinafedina/ASKME_FEDIN_ANDREY/askme_fedin/askme_fedin/askme_fedin.gunicorn.error.log' 
loglevel = 'info'
