# guide/forms.py
from django import forms
from .models import TripPlan, UserProfile

# guide/forms.py

# guide/forms.py

from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('current_place', 'bio', 'address',)  # Include other fields as needed



from django import forms
from .models import TripPlan

class TripPlanForm(forms.ModelForm):
    class Meta:
        model = TripPlan
        fields = ['destination', 'days', 'transport', 'total_price']

# guide/forms.py
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

