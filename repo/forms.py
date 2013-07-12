# -*- coding: utf-8 -*-
from django import forms

YES_OR_NO = (
    (True, 'Yes'),
    (False, 'No')
)

class SourceDataForm(forms.Form): 
    meta_file = forms.FileField(label='Select a META file for import')
    smiles_file = forms.FileField(label='Select a SMILES file for import')
    
class TestForm(forms.Form):
    input = forms.CharField(label='Input', required=False)
    