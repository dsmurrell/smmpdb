from __future__ import absolute_import

from celery import shared_task, app, task
from celery.utils.log import get_task_logger

logger = get_task_logger('repo')

import pyRserve
from django.core.mail import EmailMessage
from django.conf import settings

@task
def predict_logp(molecule_file_path, email_address):
    print molecule_file_path
    print email_address

    logger.debug('TESTING LOGGING FROM CELERY')

    conn = pyRserve.connect()
    conn.eval('library(smpredict)')
    logger.debug(conn.eval('PredictLogPtoCSV(csv.file="smlogp_predictions.csv", structures.file="' + molecule_file_path + '")'))
    logger.debug(conn.eval('getwd()'))

    mail = EmailMessage('Subject here 2', 'Here is the message 2.', 'smpredict', ['dsmurrell@gmail.com'])
    mail.attach_file('' + conn.eval('getwd()') + '/smlogp_predictions.csv')
    mail.send()
