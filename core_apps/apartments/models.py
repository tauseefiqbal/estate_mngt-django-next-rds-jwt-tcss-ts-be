from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from core_apps.common.models import TimeStampedModel
from core_apps.common.validators import validate_no_html

User = get_user_model()


class Apartment(TimeStampedModel):
    unit_number = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("Unit Number"),
        validators=[validate_no_html],
    )
    building = models.CharField(
        max_length=50,
        verbose_name=_("Building"),
        validators=[validate_no_html],
    )
    floor = models.PositiveIntegerField(
        verbose_name=_("Floor"),
        validators=[MinValueValidator(0), MaxValueValidator(200)],
    )
    tenant = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="apartment",
        verbose_name=_("Tenant"),
    )

    def __str__(self) -> str:
        return f"Unit: {self.unit_number} -  Building: {self.building} - Floor: {self.floor}"

    class Meta:
        verbose_name = _("Apartment")
        verbose_name_plural = _("Apartments")
        ordering = ["building", "floor", "unit_number"]
        indexes = [
            models.Index(fields=["building", "floor"], name="apt_building_idx"),
            models.Index(fields=["tenant"], name="apt_tenant_idx"),
        ]
