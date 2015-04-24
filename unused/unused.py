__author__ = 'daniel'

# comes from repo/views

def smlogp_file_upload(request):
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
            (out, err) = proc.communicate()
            print "output: ", out
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


def submit2(request):
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
    else:
        form = SourceDataForm() # A empty, unbound form

    # reassign the print statements to the terminal
    sys.stdout = capture.terminal

    # Render sumbit page with the documents and the form
    return render_to_response(
        'submit.html',
        {'form': form, 'output': capture.text},
        context_instance=RequestContext(request)
    )

# comes from smlogp.html
{% load bootstrap_tags %}
