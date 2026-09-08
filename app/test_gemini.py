from app.ai import extract_invoice
from .schemas import InvoiceCreate
from .models import Base, Invoice
from datetime import date, timedelta
from app.database import SessionLocal
import requests
import json

with open("emails/email2.txt", "r", encoding="utf-8") as f:
    email_text = f.read()

result = extract_invoice(email_text)

data = json.loads(result)

if data["due_date"] is None and data["due_days"] is not None:
    data["due_date"] = (
        date.today() + timedelta(days=data["due_days"])
    ).isoformat()

data["invoice_date"] = date.today().isoformat()

data.pop("due_days", None)

print(data)

# invoice = InvoiceCreate.model_validate(data)

# print("Validated invoice")
# print(invoice)

# new_invoice = Invoice(
#     supplier=invoice.supplier,
#     invoice_number=invoice.invoice_number,
#     invoice_date=invoice.invoice_date,
#     amount=invoice.amount,
#     currency=invoice.currency,
#     due_date=invoice.due_date,
# )

# db = SessionLocal()

# db.add(new_invoice)
# db.commit()
# db.refresh(new_invoice)



# Send invoice to FastAPI
response = requests.post(
    "http://127.0.0.1:8000/invoices",
    json=data
)

print("\nFastAPI response:")
print(response.status_code)
print(response.json())