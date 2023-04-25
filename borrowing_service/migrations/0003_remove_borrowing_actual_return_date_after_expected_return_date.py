from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("borrowing_service", "0002_initial"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="borrowing",
            name="actual_return_date_after_expected_return_date",
        ),
    ]
