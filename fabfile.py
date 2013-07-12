from fabric.api import *

env.hosts = ['smmpdb.ch.private.cam.ac.uk']
env.user = 'dsm38'

def prepare():
    local('python manage.py test repo')
    local('git add -p')
    local('git commit')

def deploy():
    with cd('~/smmpdb'):
        run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && git pull https://github.com/dsmurrell/smmpdb.git')
        run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && python manage.py migrate repo')
        run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && python manage.py test repo')
        run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && sudo /etc/init.d/apache2 restart')
        
def both():
    prepare()
    deploy()