# Proposal types

CONSUMER = 'consumer'
MORTGAGE = 'mortgage'
CAR_LOAN = 'car_loan'

PROPOSAL_TYPES = (
    (CONSUMER, CONSUMER.capitalize()),
    (MORTGAGE, MORTGAGE.capitalize()),
    (CAR_LOAN, CAR_LOAN.capitalize())
)

# Organization application types

NEW = 'new'
SENT = 'sent'
RECEIVED = 'received'
ACCEPTED = 'accepted'
DECLINED = 'declined'
ISSUED = 'issued'

ORGANIZATION_APPLICATION_TYPES = (
    (NEW, NEW.capitalize()),
    (SENT, SENT.capitalize()),
    (RECEIVED, RECEIVED.capitalize()),
    (ACCEPTED, ACCEPTED.capitalize()),
    (DECLINED, DECLINED.capitalize()),
    (ISSUED, ISSUED.capitalize()),
)
