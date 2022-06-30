from django import forms

class ContactForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):      
        # send email using the self.cleaned_data dictionary
        pass