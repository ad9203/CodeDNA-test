import stripe


class PaymentService:
    def process_payment(self, order_id, amount):
        for attempt in range(3):
            response = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
            )

            if response.status == "succeeded":
                return response

        return None
