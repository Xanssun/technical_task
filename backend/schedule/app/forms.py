from django import forms

from .models import Record

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['client', 'trainer', 'schedule']

    def clean(self):
        cleaned_data = super().clean()
        trainer = cleaned_data.get('trainer')
        schedule = cleaned_data.get('schedule')
        if Record.objects.filter(trainer=trainer, schedule=schedule).exists():
            raise forms.ValidationError("Эта запись уже существует.")
        return cleaned_data
