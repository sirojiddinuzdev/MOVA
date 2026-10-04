from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class PaymentService(ABC):
    
    @abstractmethod
    def create_intent(self, amount: float, currency: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a payment intent"""
        pass

    @abstractmethod
    def capture(self, intent_id: str) -> Dict[str, Any]:
        """Capture a payment intent"""
        pass

    @abstractmethod
    def refund(self, intent_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        """Refund a payment"""
        pass

    @abstractmethod
    def payout(self, seller_id: str, amount: float) -> Dict[str, Any]:
        """Payout to a seller"""
        pass


class MockPaymentProvider(PaymentService):
    
    def create_intent(self, amount: float, currency: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        return {
            "id": "mock_intent_123",
            "amount": amount,
            "currency": currency,
            "status": "requires_payment_method"
        }

    def capture(self, intent_id: str) -> Dict[str, Any]:
        return {
            "id": intent_id,
            "status": "succeeded"
        }

    def refund(self, intent_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        return {
            "id": intent_id,
            "status": "refunded",
            "amount_refunded": amount
        }

    def payout(self, seller_id: str, amount: float) -> Dict[str, Any]:
        return {
            "id": "mock_payout_123",
            "seller_id": seller_id,
            "amount": amount,
            "status": "paid"
        }
