import stripe
from django.conf import settings
from django.shortcuts import redirect

from payment_service.models import Payment
from payment_service.serializers import PaymentListSerializer

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from book_service.serializers import BookDetailSerializer
from borrowing_service.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = "__all__"


class BorrowingListSerializer(BorrowingSerializer):
    book = BookDetailSerializer(many=False, read_only=True)


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )

    def validate(self, attrs):
        book = attrs["book"]
        if book.inventory <= 0:
            raise serializers.ValidationError("Book is not available")
        return attrs

    def create(self, validated_data):
        borrowing = Borrowing.objects.create(**validated_data)
        borrowing.book.inventory -= 1
        borrowing.book.save()
        create_stripe_session_for_borrowing(borrowing)
        return borrowing

#
def create_stripe_session_for_borrowing(borrowing):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    product = stripe.Product.create(
        name=borrowing.book.title,
    )

    total_price = round(borrowing.book.daily_fee * (borrowing.expected_return_date - borrowing.borrow_date).days, 2)

    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(total_price * 100),
        currency='usd',
    )

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{
            'quantity': 1,
            "price": price.id,
        }],
        success_url="https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url='https://example.com/cancel',
    )

    payment = Payment.objects.create(
        session_id=session.id,
        session_url=session.url,
        borrowing=borrowing,
        money_to_pay=total_price,
    )

    return payment


class BorrowingDetailSerializer(BorrowingSerializer):
    payments = PaymentListSerializer(many=True, required=False)

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "payments",
        )
        read_only_fields = (
            "expected_return_date",
            "actual_return_date",
            "book",
            "payments",
        )

    def update(self, instance, validated_data):
        borrowing = Borrowing.objects.get(id=instance.id)
        if borrowing.actual_return_date:
            raise ValidationError
        borrowing.actual_return_date = timezone.now()
        borrowing.book.inventory += 1
        borrowing.save()
        borrowing.book.save()

        return redirect(self.data["payments"].get("session_url"), 302)
