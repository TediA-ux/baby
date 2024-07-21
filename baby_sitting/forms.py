from django.forms import ModelForm

from baby_sitting.models import Baby, BabySitter, BabySitting


class BabyForm(ModelForm):

    class Meta:
        model = Baby
        fields = "__all__"


class BabySitterForm(ModelForm):

    class Meta:
        model = BabySitter
        fields = "__all__"


class BabySittingForm(ModelForm):

    class Meta:
        model = BabySitting
        fields = "__all__"
