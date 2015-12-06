from __future__ import absolute_import

from celery import task
from celery.contrib import rdb
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

#@task
#def predict_NCI602(molecule_file_path, email_address):
#    print 'hello2'

@task
def import_task(source):
    capture = Capture()
    sys.stdout = capture
    importFromSource(source)
    mail = EmailMessage('Data submission report',
    capture.text, 'smpredict', ['daniel.murrell@cantab.net'])
    mail.send()

#################################################################################################
## PREDICT ON NCI60 PANEL
#################################################################################################
@task
def predict_NCI60(molecule_file_path, email_address):

    print 'in function'
    #print sys.path
    rdb.set_trace()
    #return

    #################################################################################################
    # 1. Load molecules
    #################################################################################################
    print 'blah'
    import repo.bioalerts as bioalerts
    print 'imported bioalerts'
    import os
    import numpy as np
    import sklearn
    from sklearn.ensemble import RandomForestRegressor

    try:
        print "Reading input file.\n"
        molecules = bioalerts.LoadMolecules(molecule_file_path, verbose=False)
        molecules.ReadMolecules()
        print "Total number of input molecules correctly processed: ", len(molecules.mols)
    except:
        print "ERROR: The input molecules could not be processed.\n The extension of the input file might not be supported\n"
        mail = EmailMessage('NCI60 Sensitivity Predictions',
        """Dear User,

        The requested cell line sensitivity predictions on the NCI60 panel could
        not be calculated.

        It is likely that (i) the input file was corrupted or (ii) the format of the input molecules not supported.

        Kind regards
        Cancer Cell Line Profiler team""", 'CancerCellLineProfiler', [email_address])
        mail.send()
    # Check whether the file is huge..
    if (os.path.getsize(molecule_file_path) >> 20) > 1:
        mail = EmailMessage('NCI60 Sensitivity Predictions',
        """Dear User,

        The requested cell line sensitivity predictions on the NCI60 panel could
        not be calculated because the size of the file was higher than 1Mb (maximum input file size supported).

        Kind regards
        Cancer Cell Line Profiler team""", 'CancerCellLineProfiler', [email_address])
        mail.send()

    if len(molecules.mols) == 0:
        print "ERROR: None of the input molecules was processed successfully\n"
        mail = EmailMessage('NCI60 Sensitivity Predictions',
                            """Dear User,

                            The requested cell line sensitivity predictions on the NCI60 panel could
                            not be calculated, because the input file was empty or none of the input molecules
                            was processed correctly.

                            Kind regards
                            Cancer Cell Line Profiler team""", 'CancerCellLineProfiler', [email_address])
        mail.send()
        raise
    #################################################################################################
    # 2. Calculate Morgan fps for the input molecules
    #################################################################################################
    print "Calculating Morgan fingerprints for the input molecules\n"
    mols_info = bioalerts.GetDataSetInfo()
    #mols_info.extract_substructure_information(radii=[0,1,2],mols=molecules.mols)
    fps_input_molecules = bioalerts.CalculateFPs(mols=molecules.mols,radii=[0,1,2])
    fps_input_molecules.calculate_hashed_fps(nBits=256)
    #hashed_binary = fps_input_molecules.fps_hashed_binary
    hashed_counts = fps_input_molecules.fps_hashed_counts
    mean_fps = np.load("./NCI60/server_model/mean_fps_server_NCI60.npy")
    std_fps = np.load("NCI60/server_model/std_fps_server_NCI60.npy")
    hashed_counts = (hashed_counts - mean_fps) / std_fps


    #################################################################################################
    # 3. load cell line descriptors (pathways 1000)
    #################################################################################################
    nb_input_mols = len(molecules.mols)
    cell_descs = np.genfromtxt('./NCI60/pathway_descriptors_most_var.csv',delimiter=",",skiprows=1)
    cell_names = np.genfromtxt('./NCI60/pathway_descriptors_most_var_CELL_NAMES.csv',skiprows=0,dtype="|S40")
    mean_cell_descs = np.mean(cell_descs,axis=0)
    std_cell_descs = np.std(cell_descs,axis=0)
    cell_descs = (cell_descs-mean_cell_descs) / std_cell_descs
    #cell_descs = np.repeat(cell_descs,molecules.mols,axis=0)
    # tile and repeat the cell line and compound descriptors
    hashed_counts = np.tile(hashed_counts,(59,1))
    input_mols_names = np.tile(molecules.mols_ids,(59,1))
    cell_descs = np.repeat(cell_descs,nb_input_mols,axis=0)
    cell_names = np.repeat(cell_names,nb_input_mols,axis=0)

    X = np.hstack((hashed_counts,cell_descs))

    #################################################################################################
    # 4. Load point prediction and error models
    #################################################################################################
    from sklearn.externals import joblib
    point_prediction_model = joblib.load('./NCI60/server_model/point_prediction_model_NCI60.pkl')
    error_prediction_model = joblib.load('./NCI60/server_model/error_prediction_model_NCI60.pkl')

    #################################################################################################
    # 5. Predict the activities
    #################################################################################################
    point_predictions = point_prediction_model.predict(X)
    error_prediction = error_prediction_model.predict(X)

    #################################################################################################
    # 6. Calculate the confidence intervals (70, 80, 90%)
    #################################################################################################
    alphas = np.load("./NCI60/server_model/alphas_NCI60.npy")
    alpha_70 = alphas[np.round(len(alphas)*0.7,decimals=0)]
    alpha_80 = alphas[np.round(len(alphas)*0.8,decimals=0)]
    alpha_90 = alphas[np.round(len(alphas)*0.9,decimals=0)]

    confi_70 = error_prediction * alpha_70
    confi_80 = error_prediction * alpha_80
    confi_90 = error_prediction * alpha_90

    #################################################################################################
    # 7. Write predictions to .csv
    #################################################################################################
    fich = open("./NCI60/predictions_NCI60.csv","w")
    fich.write("Cell_line\tCompound_ID\tPredicted_pGI50\tCI_70\tCI_80\tCI_90\n" %())
    for i in range(0,len(input_mols_names)):
        fich.write("%s\t%s\t%f\t%f\t%f\t%f\n" %(cell_names[i],input_mols_names[i][0],point_predictions[i],confi_70[i],confi_80[i],confi_90[i]))

    fich.close()

    #################################################################################################
    # 8. Generate plot with R of the barplot for the NCI60
    #################################################################################################
    conn = pyRserve.connect()
    logger.debug(conn.eval('source("barplot_NCI60.R")'))

    mail = EmailMessage('NCI60 Sensitivity Predictions',
                        """Dear User,

                        Thank you for using our service.
                        Here are the (i) predicted pGI50 values, and
                        (ii) the 70, 80 and 90% confidence intervals calculated with conformal prediction
                        for your input molecules.

                        In addition, you will find a pdf displaying the bioactivity profile of each input molecule across the NCI60 panel.

                        Kind regards
                        Cancer Cell Line Profiler team""", 'CancerCellLineProfiler', [email_address])
    mail.attach_file('./NCI60/predictions_NCI60.csv')
    mail.attach_file('./NCI60/predicted_profiles_NCI60.pdf')
    mail.send()

    #################################################################################################
    # 9. Remove generated files
    #################################################################################################
    import os, os.path
    if os.path.exists('./NCI60/predictions_NCI60.csv'):
        os.remove('./NCI60/predictions_NCI60.csv')

#################################################################################################
#################################################################################################
## PREDICT ON GDSC PANEL
#################################################################################################
@task
def predict_GDSC(molecule_file_path, email_address):
#################################################################################################
   # 1. Load molecules
#################################################################################################
   import repo.bioalerts as bioalerts
   import numpy as np
   import sklearn
   from sklearn.ensemble import RandomForestRegressor

   try:
      print "Reading input file.\n"
      molecules = bioalerts.LoadMolecules(molecule_file_path, verbose=False)
      molecules.ReadMolecules()
      print "Total number of input molecules correctly processed: ", len(molecules.mols)
   except:
      print "ERROR: The input molecules could not be processed.\n The extension of the input file might not be supported\n"
      mail = EmailMessage('GDSC Sensitivity Predictions',
      """Dear User,

      The requested cell line sensitivity predictions on the GDSC panel could
      not be calculated.

      It is likely that (i) the input file was corrupted or (ii) the format of the input molecules not supported.

      Kind regards
      Cancer Cell Line Profiler team""", 'CancerCellLineProfiler', [email_address])
      mail.send()
  # Check whether the file is huge..
   if (os.path.getsize(molecule_file_path) >> 20) > 1:
      mail = EmailMessage('GDSC Sensitivity Predictions',
      """Dear User,

      The requested cell line sensitivity predictions on the GDSC panel could
      not be calculated because the size of the file was higher than 1Mb (maximum input file size supported).

      Kind regards
      Cancer Cell Line Profiler team""", 'CancerCellLineProfiler', [email_address])
      mail.send()

   if len(molecules.mols) == 0:
          print "ERROR: None of the input molecules was processed successfully\n"
          mail = EmailMessage('GDSC Sensitivity Predictions',
          """Dear User,

          The requested cell line sensitivity predictions on the GDSC panel could
          not be calculated, because the input file was empty or none of the input molecules
          was processed correctly.

          Kind regards
          Cancer Cell Line Profiler team""", 'CancerCellLineProfiler', [email_address])
          mail.send()
          raise
#################################################################################################
   # 2. Calculate Morgan fps for the input molecules
#################################################################################################
   print "Calculating Morgan fingerprints for the input molecules\n"
   mols_info = bioalerts.GetDataSetInfo()
   #mols_info.extract_substructure_information(radii=[0,1,2],mols=molecules.mols)
   fps_input_molecules = bioalerts.CalculateFPs(mols=molecules.mols,radii=[0,1,2])
   fps_input_molecules.calculate_hashed_fps(nBits=256)
   #hashed_binary = fps_input_molecules.fps_hashed_binary
   hashed_counts = fps_input_molecules.fps_hashed_counts
   mean_fps = np.load("./GDSC/server_model/mean_fps_server_NCI60.npy")
   std_fps = np.load("./GDSC/server_model/std_fps_server_NCI60.npy")
   hashed_counts = (hashed_counts - mean_fps) / std_fps


#################################################################################################
   # 3. load cell line descriptors (pathways 1000)
#################################################################################################
   nb_input_mols = len(molecules.mols)
   cell_descs = np.genfromtxt('./GDSC/pathway_descriptors_most_var.csv',delimiter=",",skiprows=1)
   cell_names = np.genfromtxt('./GDSC/pathway_descriptors_most_var_CELL_NAMES.csv',skiprows=0,dtype="|S40")
   mean_cell_descs = np.mean(cell_descs,axis=0)
   std_cell_descs = np.std(cell_descs,axis=0)
   cell_descs = (cell_descs-mean_cell_descs) / std_cell_descs
   cell_descs = np.repeat(cell_descs,molecules.mols,axis=0)
   # tile and repeat the cell line and compound descriptors
   hashed_counts = np.tile(hashed_counts,(59,1))
   input_mols_names = np.tile(molecules.mol_ids,(59,1))
   cell_descs = np.repeat(cell_descs,nb_input_mols,axis=0)
   cell_names = np.repeat(cell_names,nb_input_mols,axis=0)

   X = np.hstack((hashed_counts,cell_descs))

#################################################################################################
   # 4. Load point prediction and error models
#################################################################################################
   from sklearn.externals import joblib
   point_prediction_model = joblib.load('./GDSC/server_model/point_prediction_model_GDSC.pkl')
   error_prediction_model = joblib.load('./GDSC/server_model/error_prediction_model_GDSC.pkl')

#################################################################################################
   # 5. Predict the activities
#################################################################################################
   point_predictions = point_prediction_model.predict(X)
   error_prediction = error_prediction_model.predict(X)

#################################################################################################
   # 6. Calculate the confidence intervals (70, 80, 90%)
#################################################################################################
   alphas = np.load("./GDSC/server_model/alphas_GDSC.npy")
   alpha_70 = alphas[np.round(len(alphas)*0.7,decimals=0)]
   alpha_80 = alphas[np.round(len(alphas)*0.8,decimals=0)]
   alpha_90 = alphas[np.round(len(alphas)*0.9,decimals=0)]

   confi_70 = error_prediction * alpha_70
   confi_80 = error_prediction * alpha_80
   confi_90 = error_prediction * alpha_90

#################################################################################################
   # 7. Write predictions to .csv
#################################################################################################
   fich = open("./GDSC/predictions_GDSC.csv","w")
   fich.write("Cell_line\tCompound_ID\tPredicted_pGI50\tCI_70\tCI_80\tCI_90\n" %())
   for i in range(0,len(input_mols_names)):
     fich.write("%s\t%s\t%f\t%f\t%f\t%f\n" %(cell_names[i],input_mols_names[i][0],point_predictions[i],confi_70[i],confi_80[i],confi_90[i]))
   fich.close()

#################################################################################################
   # 8. Generate plot with R of the barplot for the GDSC
#################################################################################################

   mail = EmailMessage('GDSC Sensitivity Predictions',
   """Dear User,

   Thank you for using our service.
   Here are the (i) predicted pGI50 values, and
   (ii) the 70, 80 and 90% confidence intervals calculated with conformal prediction
   for your input molecules.

   In addition, you will find a pdf displaying the bioactivity profile of each input molecule across the GDSC panel.

   Kind regards
   Cancer Cell Line Profiler team""", 'CancerCellLineProfiler', [email_address])
   mail.attach_file('./GDSC/predictions_GDSC.csv')
   #mail.attach_file('./GDSC/predicted_profiles.pdf')
   mail.send()

#################################################################################################
   # 9. Remove generated files
#################################################################################################
   import os, os.path
   if os.path.exists('./GDSC/predictions_GDSC.csv'):
       os.remove('./GDSC/predictions_GDSC.csv')

#################################################################################################

