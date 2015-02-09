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
