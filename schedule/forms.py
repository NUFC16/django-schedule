from django import forms
from schedule.models import User_profile
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field


class UserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    def __init__(self, *args, **kwargs):
        superuser = kwargs.pop("is_superuser")

        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-8'
        self.helper.render_unmentioned_fields = False
        default_layout = Layout(
            Div(
                Div(
                    'first_name',
                    'last_name',
                    'username',
                    'password1',
                    'password2',
                    css_class='col-sm-6'
                ),
                css_class='well the-fieldset row'
            ),
        )
        element=None
        if superuser:
            element = Div(
                'is_staff',
                'is_superuser',
                css_class='col-sm-6'
            )
        else:  
            element = Div(
                Field('is_staff', readonly=True, disabled=True),
                Field('is_superuser', readonly=True, disabled=True),
                css_class='col-sm-6'
            )
        default_layout[0].insert(1, element)
        self.helper.layout = default_layout

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'is_staff', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.render_unmentioned_fields = False
        self.helper.layout = Layout(
            Div(
                'user_group',
                'user_shift',
                css_class='well the-fieldset row'
            ),
        )

    class Meta:
        model = User_profile
        fields = ('user_group', 'user_shift')
