from django import forms
from schedule.models import User_profile, Group, Week_shift, Swap
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, HTML, Field, Submit
import datetime


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
        element = None
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
                'user_groups',
                'user_shift',
                'date_of_birth',
                'date_of_employment',
                'gender',
                'default_wage',
                css_class='well the-fieldset row'
            ),
        )

    class Meta:
        model = User_profile
        fields = ('user_groups', 'user_shift', 'date_of_birth',
                  'date_of_employment', 'gender', 'default_wage')


class EditUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        superuser = kwargs.pop("is_superuser")

        super(EditUserForm, self).__init__(*args, **kwargs)
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
                    css_class='col-sm-6'
                ),
                Div(
                    css_class='col-sm-6'
                ),
                css_class='well the-fieldset row'
            ),
        )
        element = None
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
        fields = ('first_name', 'last_name', 'is_staff', 'is_superuser')


class GroupForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(GroupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.render_unmentioned_fields = False
        self.helper.layout = Layout(
            Div(
                'group_name',
                'supervisor',
                css_class='well the-fieldset row'
            ),
            Submit('submit', _('Submit'))
        )

    class Meta:
        model = Group
        fields = ('group_name', 'supervisor')


class ShiftForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(ShiftForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.label_class = 'col-sm-2'
        self.helper.field_class = 'col-sm-4'
        self.helper.render_unmentioned_fields = False
        self.helper.layout = Layout(
            'name',
            Field('week_group', readonly=True, disabled=True),
            # This is needed in order to prevent user from changing group and
            # passing validation
            Field('week_group', type="hidden"),
        )

    class Meta:
        model = Week_shift
        fields = ('name', 'week_group')


class SwapForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(SwapForm, self).__init__(*args, **kwargs)
        # Custom error message
        self.fields['schedule_1'].error_messages = {
            'required': _('Pick a shift!')}
        self.fields['schedule_2'].error_messages = {
            'required': _('Pick a shift!')}

        # Crispy forms
        self.helper = FormHelper(self)
        self.helper.form_show_errors = False
        self.helper.form_tag = False
        self.helper.render_unmentioned_fields = False
        self.helper.layout = Layout(
            Field('schedule_2', template="schedule/includes/schedule_2.html"),
            HTML("<span class='swap-arrow'></span>"),
            Field('schedule_1', template="schedule/includes/schedule_1.html"),
            Field('permanent', template="schedule/includes/permanent.html")
        )

    def is_valid(self):
        valid = super(SwapForm, self).is_valid()

        # we're done now if not valid
        if not valid:
            return valid

        schedule_1 = self.cleaned_data["schedule_1"]
        if not schedule_1:
            return False

        schedule_2 = self.cleaned_data["schedule_2"]
        if not schedule_2:
            return False

        today = datetime.datetime.today().date()
        # If one of schedules is in past then dont allow it
        # If change is on the same day we are allowing it
        # If change is not on the same day then it is allowed only if one
        # of the employees is free
        if (schedule_1.date <= today) or (schedule_2.date <= today):
            if schedule_1.date <= today:
                self._errors['schedule_1'] = _("Picked date is in the past")
            if schedule_2.date <= today:
                self._errors['schedule_2'] = _("Picked date is in the past")
            return False
        elif schedule_1.date.isocalendar()[1] != schedule_2.date.isocalendar()[1]:
            self.add_error(None, forms.ValidationError(
                _("Schedules are not in the same week!"), code='invalid'))
            self._errors['schedule_1'] = _('Week %(week_num)s') % {
                'week_num': schedule_1.date.isocalendar()[1]}
            self._errors['schedule_2'] = _('Week %(week_num)s') % {
                'week_num': schedule_2.date.isocalendar()[1]}
            return False
        elif ((schedule_1.time_from != None) or (schedule_2.time_from != None)) and (schedule_1.date != schedule_2.date):
            self.add_error(None, forms.ValidationError(
                _("Picked shifts are not swapable!"), code='invalid'))
            return False

        # all good
        return True

    class Meta:
        model = Swap
        fields = ('schedule_1', 'schedule_2', 'permanent')
