from django.db import models
from django.utils.translation import gettext_lazy as _
from emissions.utils.enums import ActivityType, Unit


class Emission(models.Model):

    co2e = models.FloatField(
        null=False,
        blank=False,
        verbose_name=_("Carbon Dioxide Equivalent"),
        help_text=_("The Carbon Dioxide equivalent value."),
    )
    scope = models.PositiveIntegerField(
        verbose_name=_("Scope"),
        help_text=_("Scope."),
    )
    category = models.PositiveIntegerField(
        verbose_name=_("Category"),
        help_text=_("Category."),
        null = True,
        blank = True
    )
    activity = models.CharField(
        choices=ActivityType.choices,
        max_length=30,
        verbose_name=_("Activity"),
        help_text=_("The activity type of this emission."),
    )
    unit = models.CharField(
        choices=Unit.choices,
        max_length=10,
        verbose_name=_("Unit"),
        help_text=_("The unit of this emission."),
    )

    class Meta:
        app_label = 'emissions'

    def __str__(self):
        return self.activity
