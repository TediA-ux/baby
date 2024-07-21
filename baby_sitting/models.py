import uuid
from django.core.validators import (
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
)
from django.db import models

GENDER_MALE = "Male"
GENDER_FEMALE = "Female"

GENDER_CHOICES = [(GENDER_MALE, "Male"), (GENDER_FEMALE, "Female")]

LEVEL_OF_EDUCATION_NONE = "None"
LEVEL_OF_EDUCATION_PRIMARY = "Primary"
LEVEL_OF_EDUCATION_HIGH_SCHOOL = "High School"
LEVEL_OF_EDUCATION_BACHELORS = "Bachelor's"
LEVEL_OF_EDUCATION_MASTERS = "Masters"

LEVEL_OF_EDUCATION_CHOICES = [
    (LEVEL_OF_EDUCATION_NONE, "None"),
    (LEVEL_OF_EDUCATION_PRIMARY, "Primary"),
    (LEVEL_OF_EDUCATION_HIGH_SCHOOL, "High School"),
    (LEVEL_OF_EDUCATION_BACHELORS, "Bachelor's"),
    (LEVEL_OF_EDUCATION_MASTERS, "Masters"),
]

PERIOD_OF_STAY_HALF_DAY = "Half Day"
PERIOD_OF_STAY_FULL_DAY = "Full Day"

PERIOD_OF_STAY_CHOICES = [
    (PERIOD_OF_STAY_HALF_DAY, "Half Day"),
    (PERIOD_OF_STAY_FULL_DAY, "Full Day"),
]

HALF_DAY_FEE = 10000
FULL_DAY_FEE = 15000

PAYMENT_TYPE_BABY_SITTING = "Baby Sitting"
PAYMENT_TYPE_STORE_PURCHASE = "Store Purchase"

PAYMENT_TYPE_CHOICES = [
    (PAYMENT_TYPE_BABY_SITTING, "Baby Sitting"),
    (PAYMENT_TYPE_STORE_PURCHASE, "Store Purchase"),
]


# Create your models here.
class BabySitter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    next_of_kin_name = models.CharField(max_length=100)
    nin = models.CharField(
        max_length=14, unique=True, validators=[MinLengthValidator(14)]
    )
    recommender_name = models.CharField(max_length=100)
    religion = models.CharField(max_length=50, null=True, blank=True)
    level_of_education = models.CharField(
        max_length=50, choices=LEVEL_OF_EDUCATION_CHOICES
    )
    contact = models.CharField(max_length=10, unique=True)
    is_off_duty = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "baby_sitters"


class Baby(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    parent_name = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def latest_baby_sitting(self):
        return self.baby_sittings.order_by("-created_at").first()

    @property
    def pending_payment(self):
        baby_sitting_fees = self.baby_sittings.aggregate(
            sum=models.Sum("fee", default=0)
        )
        store_purchases_fees = self.bought_items.aggregate(
            sum=models.Sum("total_amount", default=0)
        )
        payments = self.payments.aggregate(sum=models.Sum("amount", default=0))
        last_payment = self.payments.order_by("-created_at").first()
        outstanding_filter = {}
        if last_payment:
            outstanding_filter["created_at__gt"] = last_payment.created_at

        outstanding_baby_sittings = self.baby_sittings.filter(**outstanding_filter)
        outstanding_store_purchases = self.bought_items.filter(**outstanding_filter)
        return [
            (baby_sitting_fees["sum"] + store_purchases_fees["sum"]) - payments["sum"],
            outstanding_baby_sittings,
            outstanding_store_purchases,
        ]

    class Meta:
        db_table = "babies"


class BabySitting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    baby_sitter = models.ForeignKey(
        BabySitter, models.DO_NOTHING, related_name="baby_sittings"
    )
    baby = models.ForeignKey(Baby, models.DO_NOTHING, related_name="baby_sittings")
    drop_off_person_name = models.CharField(max_length=100)
    arrival_time = models.DateTimeField()
    period_of_stay = models.CharField(max_length=8, choices=PERIOD_OF_STAY_CHOICES)
    pick_up_person_name = models.CharField(max_length=100, null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    fee = models.IntegerField(default=0, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "baby_sittings"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    baby = models.ForeignKey(Baby, models.DO_NOTHING, related_name="payments")
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payments"
