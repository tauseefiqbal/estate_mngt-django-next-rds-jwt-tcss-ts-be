from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from core_apps.common.models import TimeStampedModel
from core_apps.common.validators import sanitize_html_content, validate_content_length

User = get_user_model()


class Rating(TimeStampedModel):
    class RatingChoices(models.IntegerChoices):
        ONE = 1, _("Very Poor")
        TWO = 2, _("Poor")
        THREE = 3, _("Average")
        FOUR = 4, _("Good")
        FIVE = 5, _("Excellent")

    rated_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_ratings",
        verbose_name=_("Rated User"),
    )

    rating_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_ratings",
        verbose_name=_("Rating User"),
    )
    rating = models.IntegerField(
        choices=RatingChoices.choices, verbose_name=_("Rating")
    )
    comment = models.TextField(verbose_name=_("Comment"), blank=True)

    def __str__(self) -> str:
        return f"{self.rating_user} rates {self.rated_user} {self.rating}/5"

    def save(self, *args, **kwargs) -> None:
        # Sanitize comment content before saving
        if self.comment:
            self.comment = sanitize_html_content(self.comment)
            validate_content_length(self.comment, max_length=1000)

        # Prevent self-rating
        if self.rated_user == self.rating_user:
            raise ValueError("Users cannot rate themselves.")

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["rated_user", "-created_at"], name="rating_rated_idx"),
            models.Index(fields=["rating_user"], name="rating_user_idx"),
            models.Index(fields=["rated_user", "rating"], name="rating_score_idx"),
        ]
        unique_together = [["rated_user", "rating_user"]]
