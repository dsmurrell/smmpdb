from fabric.api import env, run, local, lcd

env.hosts = ['smmpdb.ch.private.cam.ac.uk']
env.user = 'dsm38'

def prepare():
    local('python manage.py test repo')
    local('git add -p')
    local('git commit')

def deploy():
    local('cd smmpdb $$ git pull https://github.com/dsmurrell/smmpdb.git')
    local('python manage.py migrate repo')
    local('python manage.py test repo')
    local('sudo /etc/init.d/apache2 restart')