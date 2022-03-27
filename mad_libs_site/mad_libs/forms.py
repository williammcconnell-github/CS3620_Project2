from django import forms

from .models import MadLib, WordList


class MadLibWordForm(forms.Form):
    word = forms.CharField(max_length=50, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))


class MadLibForm(forms.ModelForm):
    mad_lib_name = forms.CharField(max_length=200, label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    mad_lib_desc = forms.CharField(max_length=200, label='Description', widget=forms.TextInput(attrs={'class': 'form-control'}))
    story = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    word_list = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    number_of_input_fields = 0

    def set_number_of_input_fields(self):
        story_data = str(self.cleaned_data.get('story')).split("___")
        self.number_of_input_fields = 0
        for s in story_data:
            if s == "---":
                self.number_of_input_fields += 1

    def clean_story(self):
        self.set_number_of_input_fields()
        if self.number_of_input_fields <= 0:
            self.add_error('story', "There are no input fields in the Mad Lib Story!")
        return self.cleaned_data.get('story')

    def clean_word_list(self):
        self.set_number_of_input_fields()
        word_list_data = str(self.cleaned_data.get('word_list')).split(",")
        if self.number_of_input_fields != len(word_list_data):
            self.add_error('word_list', "The number of input words doesn't match the number of Mad Lib input fields!")
        return self.cleaned_data.get('word_list')

    class Meta:
        model = MadLib
        fields = ['mad_lib_name', 'mad_lib_desc', 'story', 'word_list']


class WordListForm(forms.ModelForm):
    mad_lib_id = forms.ModelChoiceField(queryset=MadLib.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    word = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = WordList
        fields = ['mad_lib_id', 'word', 'position']
