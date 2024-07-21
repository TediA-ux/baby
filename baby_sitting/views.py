from django.forms import modelform_factory
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from baby_sitting.forms import BabyForm, BabySitterForm, BabySittingForm
from baby_sitting.models import (
    FULL_DAY_FEE,
    HALF_DAY_FEE,
    LEVEL_OF_EDUCATION_CHOICES,
    PERIOD_OF_STAY_CHOICES,
    PERIOD_OF_STAY_HALF_DAY,
    Baby,
    BabySitter,
    BabySitting,
    Payment,
)


# Create your views here.
def babies_create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = BabyForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/babies/{form.instance.id}/")
        else:
            return render(request, "baby_form.html", {"form": form})

    return render(request, "baby_form.html", {"form": BabyForm()})


def babies_list_and_detail_view(
    request: HttpRequest, pk: str | None = None
) -> HttpResponse:
    if pk:
        return render(
            request, "baby_view.html", {"instance": get_object_or_404(Baby, pk=pk)}
        )

    return render(request, "baby_list.html", {"queryset": Baby.objects.all()})


def babies_baby_sitting_check_in(request: HttpRequest, pk: str) -> HttpResponse:
    if request.method == "POST":
        form = BabySittingForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/baby-sittings/")
        else:
            return render(request, "baby_sitting_check_in_form.html", {"form": form})

    return render(
        request,
        "baby_sitting_check_in_form.html",
        {
            "baby": get_object_or_404(Baby, pk=pk),
            "active_baby_sitters": BabySitter.objects.filter(is_off_duty=False).all(),
            "form": BabySittingForm(),
            "period_of_stay_choices": PERIOD_OF_STAY_CHOICES,
        },
    )


def baby_sitters_create_and_edit_view(
    request: HttpRequest, pk: str | None = None
) -> HttpResponse:
    if request.method == "POST":
        form = (
            BabySitterForm(
                data=request.POST, instance=get_object_or_404(BabySitter, pk=pk)
            )
            if pk
            else BabySitterForm(request.POST)
        )

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/baby-sitters/{form.instance.id}/")
        else:
            return render(
                request,
                "baby_sitter_form.html",
                {
                    "form": form,
                    "pk": pk,
                    "level_of_education_choices": LEVEL_OF_EDUCATION_CHOICES,
                },
            )

    return render(
        request,
        "baby_sitter_form.html",
        {
            "form": (
                BabySitterForm(instance=get_object_or_404(BabySitter, pk=pk))
                if pk and request.method == "GET"
                else BabySitterForm()
            ),
            "pk": pk,
            "level_of_education_choices": LEVEL_OF_EDUCATION_CHOICES,
        },
    )


def baby_sitters_list_and_detail_view(
    request: HttpRequest, pk: str | None = None
) -> HttpResponse:
    if pk:
        return render(
            request,
            "baby_sitter_view.html",
            {"instance": get_object_or_404(BabySitter, pk=pk)},
        )

    return render(
        request, "baby_sitter_list.html", {"queryset": BabySitter.objects.all()}
    )


def baby_sittings_list(request: HttpRequest) -> HttpResponse:
    return render(
        request, "baby_sitting_list.html", {"queryset": BabySitting.objects.all()}
    )


def baby_sitting_check_out(request: HttpRequest, pk: str) -> HttpResponse:
    if request.method == "POST":
        PartialBabySittingForm = modelform_factory(
            BabySitting,
            form=BabySittingForm,
            fields=("pick_up_person_name", "departure_time", "comment"),
        )
        form = PartialBabySittingForm(
            data=request.POST, instance=get_object_or_404(BabySitting, pk=pk)
        )

        if form.is_valid():
            form.save()
            form.instance.fee = (
                HALF_DAY_FEE
                if form.instance.period_of_stay == PERIOD_OF_STAY_HALF_DAY
                else FULL_DAY_FEE
            )
            form.instance.save()
            return HttpResponseRedirect(
                f"/babies/{form.instance.baby.pk}/outstandings/"
            )
        else:
            return render(request, "baby_sitting_check_out_form.html", {"form": form})

    return render(
        request,
        "baby_sitting_check_out_form.html",
        {
            "form": BabySittingForm(instance=get_object_or_404(BabySitting, pk=pk)),
        },
    )


def babies_outstandings(request: HttpRequest, pk: str) -> HttpResponse:
    baby = get_object_or_404(Baby, pk=pk)
    return render(request, "baby_outstandings.html", {"baby": baby})


def babies_pay_view(request: HttpRequest, pk: str) -> HttpResponse:
    baby = get_object_or_404(Baby, pk=pk)
    Payment.objects.create(baby=baby, amount=baby.pending_payment[0])
    return HttpResponseRedirect(f"/babies/{baby.pk}/")

def payments_list(
    request: HttpRequest
) -> HttpResponse:
    return render(request, "payments_list.html", {"queryset": Payment.objects.all()})

def Login(request):
    if request.method == 'POST':
  
        # AuthenticationForm_can_also_be_used__
  
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('index')
        else:
            messages.info(request, f'account does not exist please sign in')
    form = AuthenticationForm()
    return render(request, 'user/templates/login.html', {'form':form, 'title':'log in'})