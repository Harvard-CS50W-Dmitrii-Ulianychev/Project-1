from django import forms

class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Entry Title", widget=forms.TextInput(attrs={'placeholder': 'Enter the title...'}))
    entry_content = forms.CharField(label="Entry Text", widget=forms.Textarea(attrs={'placeholder': 'Enter the text of the entry in Markdown format...'}))

class EditEntryForm(forms.Form):
    entry_content = forms.CharField(label="Edit Entry", widget=forms.Textarea)

    def __init__(self, *args, initial_content=None, **kwargs):
        super(EditEntryForm, self).__init__(*args, **kwargs)
        if initial_content:
            self.fields['entry_content'].initial = initial_content