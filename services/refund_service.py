import stripe
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class RefundService:
    def __init__(self, stripe_client=None):
        self.stripe_client = stripe_client or stripe

    def process_refund(self, payment_id, amount, reason="requested_by_customer"):
        """Process a refund for an existing payment."""

        if not payment_id:
            raise ValueError("Payment ID is required")

        if amount <= 0:
            raise ValueError("Refund amount must be greater than zero")

        try:
            logger.info(
                "Starting refund for payment=%s amount=%s",
                payment_id,
                amount,
            )

            refund = self.stripe_client.Refund.create(
                payment_intent=payment_id,
                amount=amount,
                reason=reason,
            )

            if refund.status == "succeeded":
                logger.info(
                    "Refund completed successfully for payment=%s",
                    payment_id,
                )

                return {
                    "success": True,
                    "refund_id": refund.id,
                    "payment_id": payment_id,
                    "amount": amount,
                    "created_at": datetime.utcnow().isoformat(),
                }

            logger.warning(
                "Refund did not succeed for payment=%s status=%s",
                payment_id,
                refund.status,
            )

            return {
                "success": False,
                "refund_id": getattr(refund, "id", None),
                "payment_id": payment_id,
                "amount": amount,
                "status": refund.status,
            }

        except Exception as exc:
            logger.error(
                "Refund failed for payment=%s amount=%s error=%s",
                payment_id,
                amount,
                exc,
            )

            return {
                "success": False,
                "payment_id": payment_id,
                "amount": amount,
                "error": str(exc),
            }

    def get_refund(self, refund_id):
        """Retrieve a previously created refund."""

        if not refund_id:
            raise ValueError("Refund ID is required")

        try:
            refund = self.stripe_client.Refund.retrieve(refund_id)

            return {
                "id": refund.id,
                "status": refund.status,
                "amount": refund.amount,
                "payment_intent": refund.payment_intent,
            }

        except Exception as exc:
            logger.error(
                "Unable to retrieve refund=%s error=%s",
                refund_id,
                exc,
            )
            return None

    def cancel_refund(self, refund_id):
        """Cancel a pending refund when supported by the payment provider."""

        if not refund_id:
            raise ValueError("Refund ID is required")

        try:
            refund = self.stripe_client.Refund.cancel(refund_id)

            logger.info(
                "Refund cancellation requested for refund=%s status=%s",
                refund_id,
                refund.status,
            )

            return {
                "success": True,
                "refund_id": refund.id,
                "status": refund.status,
            }

        except Exception as exc:
            logger.error(
                "Refund cancellation failed for refund=%s error=%s",
                refund_id,
                exc,
            )

            return {
                "success": False,
                "refund_id": refund_id,
                "error": str(exc),
            }
