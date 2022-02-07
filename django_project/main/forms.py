from django import forms
from .models import InputPeter, InputMary
# csv export function
from django.utils.translation import gettext_lazy as _
from django.forms import widgets

pw_products = [
    ('fp', 'FasterPay'),
    ('pw', 'Paymentwall'),
    ('', 'All'),
]

run_types = [
    ('one_time', 'One-off Task'),
    ('scheduled', 'Scheduled Task'),
]

keyword_logic = [
    ('AND', 'AND'),
    ('OR', 'OR'),
]


class InputPeterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = InputPeter
        fields = ['domain', 'keywords', 'keyword_logic', 'input_id']
        labels = {
            'domain': 'Domain to Search for',
            'keywords': 'Keywords',
            'keyword_logic': 'Searching Logic for Keywords',
            # 'input_id': 'Input UUID'
        }
        widgets = {'input_id': forms.HiddenInput(),
                   'keywords': forms.TextInput(attrs={'placeholder': 'Keyword1, Keyword2, etc.'}),
                   'keyword_logic': forms.Select(choices=keyword_logic),
                   }
        required = ['domain']


class InputMaryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True

    class Meta:
        model = InputMary
        fields = ['run_type', 'pw_product', 'merchant_id',
                  'merchant_name', 'project_id', 'project_name',
                  'keywords', 'keyword_logic', 'input_id']
        labels = {
            'run_type': 'Run Type (One-off or Scheduled Task)',
            'pw_product': 'Company Product',
            'merchant_id': 'Merchant ID (Paymentwall or Fasterpay)',
            'merchant_name': 'Merchant Name (Paymentwall or Fasterpay)',
            'project_id': 'Project ID (Paymentwall only)',
            'project_name': 'Project Name (Paymentwall only)',
            'keywords': 'Keywords',
            'keyword_logic': 'Searching Logic for Keywords',
            'input_id': 'Input UUID'
        }
        widgets = {'input_id': forms.HiddenInput(),
                   'run_type': forms.Select(choices=run_types),
                   'pw_product': forms.Select(choices=pw_products),
                   'keywords': forms.TextInput(attrs={'placeholder': 'Keyword1, Keyword2, etc.'}),
                   'keyword_logic': forms.Select(choices=keyword_logic),
                   }
        required = []


###### CSV　EXPORT FUNCTION
class CheckboxSelectAll(widgets.CheckboxSelectMultiple):
    """
    Add a select-all-checkbox for the CheckboxSelectMultiple-widget.
    """

    template_name = 'django/forms/widgets/checkbox_select_all.html'

    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'csvexport/checkbox_select_all.js')


class CSVFieldsForm(forms.Form):
    """
    A form holding the fields of models as multiple-choice-fields.
    Fields are added dynamically. At least one option of all fields must be
    checked.
    """
    ERR_MSG = "Model-fields must be selected in order to export them."

    def clean(self):
        """
        At least one option of one multiple-choice-field must be checked.
        """
        cleaned_data = super().clean()

        if not any(f for f in cleaned_data.values()):
            raise forms.ValidationError(self.ERR_MSG)

        return cleaned_data


class UniqueForm(forms.Form):
    unique = forms.BooleanField(
        label=_('Unique rows'),
        help_text=_("If checked all rows of the result data will be unique."),
        required=False
    )


class CSVFormatForm(forms.Form):
    delimiter = forms.CharField(
        label=_('Delimiter'),
        help_text=_("A one-character string used to separate fields."),
        widget=forms.TextInput(attrs={'maxlength': 1}),
        required=False
    )
    escapechar = forms.CharField(
        label=_('Escapechar'),
        help_text=_("A one-character string to escape the delimiter and "
                    "the quotechar if doublequote is False."),
        widget=forms.TextInput(attrs={'maxlength': 1}),
        required=False
    )
    lineterminator = forms.CharField(
        label=_('Lineterminator'),
        help_text=_("The string used to terminate lines."),
        widget=forms.TextInput(),
        required=False
    )
    quotechar = forms.CharField(
        label=_('Quotechar'),
        help_text=_("A one-character string used to quote fields."),
        widget=forms.TextInput(attrs={'maxlength': 1}),
        required=False
    )
    doublequote = forms.BooleanField(
        label=_('Doublequote'),
        help_text=_("Controls how instances of quotechar appearing inside a "
                    "field should themselves be quoted. When True, the "
                    "character is doubled. When False, the escapechar "
                    "is used as a prefix to the quotechar."),
        required=False
    )
    quoting = forms.ChoiceField(
        label=_("Quoting"),
        choices=(
            ('QUOTE_ALL', _('Quote All')),
            ('QUOTE_MINIMAL', _('Quote Minimal')),
            ('QUOTE_NONNUMERIC', _('Quote Non-Numeric')),
            ('QUOTE_NONE', _('Quote None')),
        ),
        help_text=_("Controls how fields should be quoted."),
        required=False
    )
