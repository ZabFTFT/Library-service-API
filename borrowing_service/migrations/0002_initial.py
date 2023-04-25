from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("borrowing_service", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="borrowing",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name="borrowing",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("borrow_date__lte", models.F("expected_return_date"))
                ),
                name="borrow_date_before_expected_return_date",
            ),
        ),
        migrations.AddConstraint(
            model_name="borrowing",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("expected_return_date__gte", models.F("borrow_date"))
                ),
                name="expected_return_date_after_borrow_date",
            ),
        ),
        migrations.AddConstraint(
            model_name="borrowing",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("actual_return_date__isnull", True),
                    ("actual_return_date__gte", models.F("borrow_date")),
                    _connector="OR",
                ),
                name="actual_return_date_after_borrow_date",
            ),
        ),
        migrations.AddConstraint(
            model_name="borrowing",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("actual_return_date__isnull", True),
                    (
                        "actual_return_date__gte",
                        models.F("expected_return_date"),
                    ),
                    _connector="OR",
                ),
                name="actual_return_date_after_expected_return_date",
            ),
        ),
    ]
