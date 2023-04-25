from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("book_service", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow_date", models.DateTimeField(auto_now_add=True)),
                ("expected_return_date", models.DateTimeField()),
                ("actual_return_date", models.DateTimeField(null=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="book_service.book",
                    ),
                ),
            ],
            options={
                "default_related_name": "borrowings",
            },
        ),
    ]
