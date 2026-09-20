"""
InfraFlow Integration Adapters

Clean interfaces representing external integrations (PFMS, eOffice, eProcurement, eSign).
For MVP, mock implementations are used.
"""

class BasePaymentGateway:
    def initiate_disbursement(self, payment_id, amount, account_details):
        raise NotImplementedError

class MockPFMSPaymentGateway(BasePaymentGateway):
    def initiate_disbursement(self, payment_id, amount, account_details):
        import uuid
        return {
            "status": "SUCCESS",
            "utr_number": f"PFMSUTR{uuid.uuid4().hex[:10].upper()}",
            "message": "Disbursement instruction processed successfully via Mock PFMS Adapter"
        }

class BaseDigitalSignatureProvider:
    def sign_document(self, document_id, signer_id):
        raise NotImplementedError

class MockDigitalSignatureProvider(BaseDigitalSignatureProvider):
    def sign_document(self, document_id, signer_id):
        import uuid
        return {
            "status": "SIGNED",
            "signature_hash": f"DSCHASH-{uuid.uuid4().hex[:16].upper()}",
            "timestamp": "2026-09-20T12:00:00Z"
        }
