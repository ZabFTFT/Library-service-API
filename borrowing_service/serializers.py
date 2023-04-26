import stripe
from django.conf import settings

from payment_service.models import Payment
from payment_service.serializers import PaymentListSerializer

import datetime


from django_q.tasks import async_task
from rest_framework import serializers

from book_service.serializers import BookDetailSerializer
from borrowing_service.models import Borrowing

from notification.notifications import send_notification


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

    def _create_message(self, validated_data):
        customer = self.context.get("request").user
        book = validated_data.get("book").title
        expected_return_date = validated_data.get(
            "expected_return_date"
        ).strftime("%Y-%m-%d %H:%M")
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        message_text = (
            "Borrowing!\n"
            f"user: {customer.email}\n"
            f"took: {book}\n"
            f"borrow date: {current_date}\n"
            f"expected return date: {expected_return_date}\n"
        )

        return message_text

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
        message_text = self._create_message(validated_data)
        async_task(send_notification(message_text))
        return borrowing


def create_stripe_session_for_borrowing(borrowing):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    product = stripe.Product.create(
        name=borrowing.book.title,
    )

    total_price = round(
        borrowing.book.daily_fee
        * (borrowing.expected_return_date - borrowing.borrow_date).days,
        2,
    )

    price = stripe.Price.create(
        product=product.id,
        unit_amount=int(total_price * 100),
        currency="usd",
    )

    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "quantity": 1,
                "price": price.id,
            }
        ],
        success_url="https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://example.com/cancel",
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
