from __future__ import absolute_import

from celery import shared_task, app, task

import pyRserve

@task
def predict_logp(molecule_file_path, email_address):
    print molecule_file_path
    print email_address

    conn = pyRserve.connect()
    #conn.eval('library(smpredict)')
    #print conn.eval('PredictLogPtoCSV(csv.file="smlogp_predictions.csv", structures.file="' + molecule_file_path + '")')

    print conn.eval('getwd()')
