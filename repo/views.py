# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
import subprocess

from repo.models import SourceData, MoleculeFile
from repo.forms import *

from utils import *

def list(request):
    capture = Capture()
    # make all print statements go to the text field in the capture object
    sys.stdout = capture
    
    # Handle file upload
    if request.method == 'POST':
        form = SourceDataForm(request.POST, request.FILES)
        if form.is_valid():
            source_data = SourceData(smiles_file = request.FILES['smiles_file'], meta_file = request.FILES['meta_file'])
            source_data.save()
            
            print source_data.smiles_file
            print source_data.meta_file
            
            importFromSourceData(source_data)

            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('repo.views.list'))
    else:
        form = SourceDataForm() # A empty, unbound form
        
    # reassign the print statements to the terminal 
    sys.stdout = capture.terminal

    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'form': form, 'output': capture.text},
        context_instance=RequestContext(request)
    )

def smlogp2(request):
    # Render smlogp page 
    return render_to_response(
        'smlogp.html',
        context_instance=RequestContext(request)
    )

def smlogp(request):
    capture = Capture()
    # make all print statements go to the text field in the capture object
    sys.stdout = capture
    
    # Handle file upload
    if request.method == 'POST':
        form = MoleculeFileForm(request.POST, request.FILES)
        if form.is_valid():
            input = form.cleaned_data['input']
            #os.chdir('/home/dsm38/smmpdb')
            print os.getcwd()
            proc = subprocess.Popen(["Rscript predictSMILES.R " + input], stdout=subprocess.PIPE, shell=True)
            
            #proc = subprocess.Popen(["pwd"], stdout=subprocess.PIPE, shell=True)
            (out, err) = proc.communicate()
            print "output: ", out 
            #print "LogP Prediction:", out.split('\n')[-2].split(" ")[-1]
            
            #os.system("pwd")
            #molecule_file = MoleculeFile(molecule_file = request.FILES['molecule_file'])
            #molecule_file.save()
            
            #print molecule_file.molecule_file
            
            #importFromSourceData(source_data) DO SOMETHING HERE

            # Redirect to the document list after POST
            #return HttpResponseRedirect(reverse('repo.views.list'))
    else:
        form = MoleculeFileForm() # A empty, unbound form
        
    # reassign the print statements to the terminal 
    sys.stdout = capture.terminal

    # Render list page with the documents and the form
    return render_to_response(
        'smlogp.html',
        {'form': form, 'output': capture.text},
        context_instance=RequestContext(request)
    )

def test(request):
    capture = Capture()
    # make all print statements go to the text field in the capture object
    sys.stdout = capture
    
    # Handle file upload
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data['input']
            
            if 'print_input' in request.POST:
                print input
                
            if 'delete_source' in request.POST:
                deleteSource(input)
            
            if 'print_compound_duplicates' in request.POST:
                if input != "":
                    printMultipleMeasurementsOfType(input)
                else:
                    printMultipleMeasurements()
                
            if 'print_compound_hanging' in request.POST:
                printNoMeasurements()
                
            if 'dump_multiple_sources' in request.POST:
                dump_multiple_sources(input)
    else:
        form = TestForm() # A empty, unbound form
        
    # reassign the print statements to the terminal 
    sys.stdout = capture.terminal

    # Render list page with the documents and the form
    return render_to_response(
        'test.html',
        {'form': form, 'output': capture.text},
        context_instance=RequestContext(request)
    )