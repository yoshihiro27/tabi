from django import forms
from .models import Tabi,TabiDate,Comment





class TabiCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Tabi
        fields = ['title','text','money','date','thumbnail']

class TabiDateForm(forms.ModelForm):
    class Meta:
        model = TabiDate
        fields = '__all__'

TabiDateFormset = forms.inlineformset_factory(
    Tabi, TabiDate,TabiDateForm, extra=1, 
)

'''
TabiDateFormset = forms.inlineformset_factory(
    Tabi, TabiDate, fields='__all__',
    extra=3, max_num=5, can_delete=False
)
'''

class TabiSearchForm(forms.Form):
    key_word = forms.CharField(
        label='キーワード',required=False,
        widget=forms.TextInput(attrs={'class': 'input'})
    )


class SearchForm(forms.Form):

    tags = forms.CharField(
        initial='',
        label='タイトル',
        required = False, # 必須ではない
    )
    
class CommentCreateForm(forms.ModelForm):
    """コメント投稿フォーム"""

    class Meta:
        model = Comment
        fields = ('text',)