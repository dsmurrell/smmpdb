from __future__ import absolute_import

from celery import shared_task, app, task
from celery.utils.log import get_task_logger

from utils import importFromSource, Capture
import sys

logger = get_task_logger('repo')

import pyRserve
from django.core.mail import EmailMessage

@task
def predict_logp(molecule_file_path, email_address):
    print molecule_file_path
    print email_address

    logger.debug('TESTING LOGGING FROM CELERY')

    conn = pyRserve.connect()
    conn.eval('library(smpredict)')
    logger.debug(conn.eval('PredictPropertytoCSV("LogP", csv.file="smlogp_predictions.csv", structures.file="' + molecule_file_path + '", error.variance=TRUE)'))
    logger.debug(conn.eval('getwd()'))

    mail = EmailMessage('Your LogP Predictions',
    """Dear User

Thank you for using our service.
here are your LogP predictions.

Kind regards
smpredict team""", 'smpredict', [email_address])
    mail.attach_file('' + conn.eval('getwd()') + '/smlogp_predictions.csv')
    mail.send()

@task
def predict_logs(molecule_file_path, email_address):
    print molecule_file_path
    print email_address

    logger.debug('TESTING LOGGING FROM CELERY')

    conn = pyRserve.connect()
    conn.eval('library(smpredict)')
    logger.debug(conn.eval('PredictPropertytoCSV("LogS", csv.file="predictions.csv", structures.file="' + molecule_file_path + '", error.variance=TRUE)'))
    logger.debug(conn.eval('getwd()'))

    mail = EmailMessage('Your LogS Predictions',
    """Dear User

Thank you for using our service.
here are your LogS predictions.

Kind regards
smpredict team""", 'smpredict', [email_address])
    mail.attach_file('' + conn.eval('getwd()') + '/predictions.csv')
    mail.send()

@task
def import_task(source):
    capture = Capture()
    sys.stdout = capture
    importFromSource(source)
    mail = EmailMessage('Data submission report',
    capture.text, 'smpredict', ['daniel.murrell@cantab.net'])
    mail.send()

