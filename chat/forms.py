from django import forms


class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={
                        "cols":"1",
                        "rows":"1", 
                        "placeholder":"Your Message" 
                    }
                )
            )