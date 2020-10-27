from decimal import Decimal

from decimal import Decimal

from django import forms
from django.forms import ModelForm

from expert.models import Expert
from .models import Event, Category, Ticket, AggrEvents
from django.forms.widgets import TextInput


# # TODO customize form validation errors
# class EventForm(forms.ModelForm):
#     name = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={'id': 'name', 'class': 'form-control', 'placeholder': 'Name your event'})
#     )
#     organizer = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={'id': 'organizer', 'class': 'form-control', 'placeholder': 'Organizer Name'})
#     )
#     category = forms.ModelChoiceField(
#         required=True,
#         queryset=Category.objects.all(),
#         empty_label=None,
#         to_field_name="name",
#         widget=forms.Select(attrs={'id': 'category', 'class': 'form-control selectpicker', 'data-live-search': 'true'})
#     )
#     speaker = forms.ModelChoiceField(
#         required=True,
#         queryset=Expert.objects.all(),
#         empty_label=None,
#         to_field_name="name",
#         widget=forms.Select(attrs={'id': 'speaker', 'class': 'form-control selectpicker', 'data-live-search': 'true'})
#     )
#     event_img = forms.ImageField(
#         required=True,
#     )
#     ticket_type = forms.ChoiceField(
#         required=True,
#         choices=(
#             ("Paid", ("Paid")),
#             ("Free", ("Free")),
#             ("Donation", ("Donation"))
#         )
#     )
#     price = forms.DecimalField(
#         label='Price',
#         required=True,
#         min_value=Decimal('0.00'),
#         widget=forms.NumberInput(attrs={'id': 'price', 'class': 'form-control', 'placeholder': '$ 0.00'})
#     )
#     quantity = forms.DecimalField(
#         label='Quantity',
#         required=True,
#         min_value=Decimal('0'),
#         widget=forms.NumberInput(
#             attrs={'id': 'quantity', 'class': 'form-control', 'placeholder': 'Quantity'})
#     )
#     info = forms.CharField(
#         required=True,
#         widget=forms.Textarea(attrs={'id': 'description', 'class': 'form-control', 'rows': '4'})
#     )
#     start_event_dt = forms.DateTimeField(
#         required=True,
#         widget=forms.DateInput(attrs={'class': 'form-control'})
#     )
#     finish_event_dt = forms.DateTimeField(
#         widget=forms.DateInput(attrs={'class': 'form-control'})
#     )
#     location = forms.CharField(
#         required=True,
#         widget=forms.TextInput(
#             attrs={'id': 'location', 'class': 'form-control', 'placeholder': 'Sample Conference Center, City, Country'})
#     )
#
#     # def clean_price(self):
#     #     if  self.cleaned_data['ticket_type'] == 'Free':
#     #         self.cleaned_data['price'] = 22
#
#     class Meta:
#         model = Event
#         exclude = ['cdate']
#         widgets = {
#             'language': forms.Select(attrs={'id': 'lang', 'class': 'form-control'}),
#             'event_img': forms.FileInput(attrs={'id': 'the-file', 'class': 'form-control-file form-control'})
#         }


# TODO customize form validation errors
class EventForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'id': 'ep-ce-event-name', 'name': 'ep-ce-event-name',
                                      'class': 'form-control jb-input-w', 'placeholder': 'Name your event'})
    )
    # organizer = forms.CharField(
    #     required=True,
    #     widget=forms.TextInput(attrs={'id': 'organizer', 'class': 'form-control', 'placeholder': 'Organizer Name'})
    # )
    # category = forms.ModelChoiceField(
    #     required=True,
    #     queryset=Category.objects.all(),
    #     empty_label=None,
    #     to_field_name="name",
    #     widget=forms.Select(attrs={'id': 'category', 'class': 'form-control selectpicker', 'data-live-search': 'true'})
    # )
    # speaker = forms.ModelChoiceField(
    #     required=True,
    #     queryset=Expert.objects.all(),
    #     empty_label=None,
    #     to_field_name="name",
    #     widget=forms.Select(attrs={'id': 'speaker', 'class': 'form-control selectpicker', 'data-live-search': 'true'})
    # )
    event_img = forms.ImageField(
        required=False,
    )
    # ticket_type = forms.ChoiceField(
    #     required=True,
    #     choices=(
    #         ("Paid", ("Paid")),
    #         ("Free", ("Free")),
    #         ("Donation", ("Donation"))
    #     )
    # )
    # price = forms.DecimalField(
    #     label='Price',
    #     required=True,
    #     min_value=Decimal('0.00'),
    #     widget=forms.NumberInput(attrs={'id': 'price', 'class': 'form-control', 'placeholder': '$ 0.00'})
    # )
    # quantity = forms.DecimalField(
    #     label='Quantity',
    #     required=True,
    #     min_value=Decimal('0'),
    #     widget=forms.NumberInput(
    #         attrs={'id': 'quantity', 'class': 'form-control', 'placeholder': 'Quantity'})
    # )
    info = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'id': 'ep-ce-event-info',
            'class': 'form-control jb-input-w p-3',
            'rows': '5',
            'cols': '50',
        })
    )
    start_event_dt = forms.DateTimeField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control jb-input-w p-2',
            'id': 'ep-ce-event-sdate',
            'autocomplete': 'off',
            'data-provide': 'datepicker',
            'data-date-format': 'yyyy-mm-dd',
        })
    )
    finish_event_dt = forms.DateTimeField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control jb-input-w p-2',
            'id': 'ep-ce-event-edate',
            'autocomplete': 'off',
            'data-provide': 'datepicker',
            'data-date-format': 'yyyy-mm-dd',
        })
    )
    location = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={'id': 'ep-ce-event-loc', 'class': 'form-control jb-input-w',
                   'placeholder': 'City, Country'})
    )
    ticket_url = forms.CharField(
        required=False,
        widget=forms.URLInput(
            attrs={'id': 'exp_fb_link',
                   'class': 'form-control jb-input-w'
                   }
        )
    )
    refund_policy_url = forms.CharField(
        required=False,
        widget=forms.URLInput(
            attrs={'id': 'ep-ce-lrefund',
                   'class': 'form-control jb-input-w',
                   'placeholder': 'https://www.site.com/'
                   }
        )
    )
    contact_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'id': 'ep-ce-contactemail',
                   'class': 'form-control jb-input-w',
                   'placeholder': 'contact@email.com'
                   }
        )
    )

    # def clean_price(self):
    #     if  self.cleaned_data['ticket_type'] == 'Free':
    #         self.cleaned_data['price'] = 22

    class Meta:
        model = Event
        # exclude = ['cdate']
        fields = [
            'name',
            'no_refund',
            'event_img',
            'info',
            'start_event_dt',
            'finish_event_dt',
            'location',
            'ticket_url',
            'refund_policy_url',
            'contact_email',
        ]
        widgets = {
            # 'language': forms.Select(attrs={'id': 'lang', 'class': 'form-control'}),
            # 'event_img': forms.FileInput(attrs={'id': 'the-file', 'class': 'form-control-file form-control'}),
            'no_refund': forms.CheckboxInput(attrs={'id': 'ep-ce-norefund',
                'onchange': 'noRefund()'}),
        }


class TicketForm(forms.ModelForm):
    # # TODO clean methodsss
    # price = forms.IntegerField()
    # def clean_price(self):
    #     price = self.cleaned_data['price']
    #     if price < 0:
    #         raise forms.ValidationError("Price can't be negative")

    class Meta:
        model = Ticket
        exclude = ['ticket']


class BuyTicketForm(forms.ModelForm):
    # TODO add validation for quota and quantity relation, free = 0 
    quantiy = forms.DecimalField(
        label='Quantity',
        required=False,
        min_value=Decimal('0')
    )
    donation_price = forms.DecimalField(
        label='Price',
        required=False,
        min_value=Decimal('0.00')
    )
    quota_left = forms.DecimalField(
        disabled=True,
        required=False,
        min_value=Decimal('0')
    )

    class Meta:
        model = Ticket
        fields = ('quota_left',)
        # exclude = ['event']
    # clean_quantity(self):
    #     data = self.cleaned_data["quantity"]
    #     if data < 

    #     return data


class AggrEventsForm(ModelForm):
    class Meta:
        model = AggrEvents
        fields = '__all__'
        widgets = {
            'bg_color': TextInput(attrs={'type':'color'})
        }
