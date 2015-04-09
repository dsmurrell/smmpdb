# -*- coding: utf-8 -*-
from django import forms

YES_OR_NO = (
    (True, 'Yes'),
    (False, 'No')
)

class SourceDataForm(forms.Form):
    email_address = forms.EmailField(label='Submitter''s email address', required=True)
    display_name = forms.CharField(label='Display Name', required=True)
    url = forms.CharField(label='URL', required=True)
    description = forms.CharField(label='description', required=True)
    meta_file = forms.FileField(label='Select a META file for import', required=True)
    smiles_file = forms.FileField(label='Select a SMILES file for import', required=True)
    
class TestForm(forms.Form):
    input = forms.CharField(label='Input', required=False)
    
class MoleculeFileForm(forms.Form):
    email_address = forms.EmailField(label='Please enter your email address', required=True)
    molecule_file = forms.FileField(label='Please select your SDF or SMILES file', required=True)