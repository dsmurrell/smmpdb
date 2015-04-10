# -*- coding: utf-8 -*-
from django import forms

YES_OR_NO = (
    (True, 'Yes'),
    (False, 'No')
)

class SourceForm(forms.Form):
    email_address = forms.EmailField(label='Submitter''s email address', required=True)
    name = forms.CharField(label='Datasource Name', required=True)
    url = forms.CharField(label='External Link (URL)', required=True)
    description = forms.CharField(label='Short Description', required=True)
    meta_file = forms.FileField(label='Select a META file for import', required=True)
    smiles_file = forms.FileField(label='Select a SMILES file for import', required=True)
    
class TestForm(forms.Form):
    input = forms.CharField(label='Input', required=False)
    
class MoleculeFileForm(forms.Form):
    email_address = forms.EmailField(label='Please enter your email address', required=True)
    molecule_file = forms.FileField(label='Please select your SDF or SMILES file', required=True)