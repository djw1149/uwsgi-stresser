import uwsgi
import os


import uwsgi_stress.api
import uwsgi_stress.auth

print('Loading... in pid', os.getpid())
noauth = uwsgi_stress.auth.noauth(uwsgi_stress.api.STRESS())

