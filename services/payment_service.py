import stripe
import logging


logger = logging.getLogger(__name__)


class PaymentService:
    def process_payment(self, order_id, amount):
        for attempt in range(3):
            try:
                logger.info(
                    "Processing payment order=%s attempt=%s",
                    order_id,
                    attempt + 1,
                )

                response = stripe.PaymentIntent.create(
                    amount=amount,
                    currency="usd",
                )

                if response.status == "succeeded":
                    logger.info(
                        "Payment succeeded order=%s",
                        order_id,
                    )
                    return response

            except Exception as exc:
                logger.error(
                    "Payment failed order=%s error=%s",
                    order_id,
                    exc,
                )

        return None

    def get_payment(self, payment_id):
        try:
            payment = stripe.PaymentIntent.retrieve(payment_id)

            return {
                "id": payment.id,
                "status": payment.status,
                "amount": payment.amount,
            }

        except Exception as exc:
            logger.error(
                "Unable to retrieve payment=%s error=%s",
                payment_id,
                exc,
            )
            return None

    def cancel_payment(self, payment_id):
        try:
            payment = stripe.PaymentIntent.cancel(payment_id)

            logger.info(
                "Payment cancellation requested payment=%s",
                payment_id,
            )

            return payment

        except Exception as exc:
            logger.error(
                "Payment cancellation failed payment=%s error=%s",
                payment_id,
                exc,
            )
            return None
