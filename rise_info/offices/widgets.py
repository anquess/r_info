from django import forms


class OfficeSuggestWidget(forms.SelectMultiple):
    template_name = 'offices/widgets/suggest.html'

    class Media:
        js = ['offices/js/suggest.js']
        css = {
            'all': ['offices/css/suggest.css']
        }

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += 'suggest'
        else:
            self.attrs['class'] = 'suggest'
