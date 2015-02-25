from fabric.api import *

env.hosts = ['smmpdb.ch.private.cam.ac.uk']
env.user = 'dsm38'

def prepare():
    local('python manage.py collectstatic --noinput')
    local('python manage.py test repo')
    local('echo "another line" >> fillfile')
    local('git add .')
    local('git commit')
    local('git push')

def deploy():
    with cd('~/smmpdb'):
        run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && git pull https://github.com/dsmurrell/smmpdb.git')
        run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && sudo pip install -r requirements.txt')
        run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && python manage.py migrate')
        #run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && sudo pkill celery')
        run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && sudo celery -A smmpdb worker -l info &')
        run('source /home/dsm38/.virtualenvs/smmpdb/bin/activate && sudo /etc/init.d/apache2 restart')
        
def both():
    prepare()
    deploy()
    
def bothwarn():
    with settings(warn_only=True):
        prepare()
        deploy()
