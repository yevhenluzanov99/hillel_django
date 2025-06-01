from django.db import models
from django.utils.translation import gettext_lazy as _


class Position(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=200)
    is_manager = models.BooleanField(default=False, verbose_name=_("Is Manager"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    department = models.ForeignKey(
        "Department", on_delete=models.CASCADE, verbose_name=_("Department")
    )
    description = models.CharField(
        verbose_name=_("Job Description"), max_length=500, default=""
    )
    monthly_rate = models.IntegerField(default=0, verbose_name=_("Monthly Rate"))

    def __str__(self):
        return f"{self.title} ({self.department})"
