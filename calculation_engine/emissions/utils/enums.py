from django.db import models
from django.utils.translation import gettext_lazy as _


class ActivityType(models.TextChoices):
    PERSONAL_TRAVEL = "PERSONAL_TRAVEL", _("Personal travel")
    AIR_TRAVEL = "AIR_TRAVEL", _("Air travel")
    PURCHASED_GOODS_AND_SERVICES = "PURCHASED_GOODS_AND_SERVICES", _("Purchased goods and services")
    ELECTRICITY = "ELECTRICITY", _("Electricity")


class Unit(models.TextChoices):
    GBP = "GBP", _("GBP")
    KILOMETRES = "KILOMETRES", _("KILOMETRES")
    KWH = "KWH", _("KWH")
    MILES = "MILES", _("MILES")

