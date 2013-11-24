from django import forms
from django.utils.translation import ugettext_lazy as _

from playerproject.apps.dashboard.models import PPUserRecord
from playerproject.libs.fields import SubmitButtonField

class PPUserRecordForm(forms.ModelForm):
    submit = SubmitButtonField(label="", initial=u"Create Record")

    class Meta:
        fields = ['first_name', 'last_name']
        model = PPUserRecord