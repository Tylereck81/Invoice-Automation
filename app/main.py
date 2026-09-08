from fastapi import FastAPI, Depends 
from sqlalchemy.orm import Session 

from .database import engine, SessionLocal
from .models import Base, Invoice
from .schemas import InvoiceCreate

import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine) 

app = FastAPI() 

def get_db(): 
    db = SessionLocal() 

    try:
        yield db 
    finally:
        db.close()


@app.post("/invoices")
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    start = time.perf_counter()
    
    logger.info("Received invoice: %s", invoice.invoice_number)

    logger.info("Invoice passed validation")

    new_invoice = Invoice(  
        supplier=invoice.supplier,
        invoice_number=invoice.invoice_number,
        invoice_date=invoice.invoice_date,
        amount=invoice.amount,
        currency=invoice.currency
    )

    logger.info(
        "Created database object | %.4f sec",
        time.perf_counter() - start
    )
    
    db.add(new_invoice)

    logger.info(
        "Added invoice to database session | %.4f sec",
        time.perf_counter() - start
    )

    db.commit()

    logger.info(
        "Committed invoice to PostgreSQL | %.4f sec",
        time.perf_counter() - start
    )

    db.refresh(new_invoice)

    logger.info(
        "END processing invoice %s | total %.4f sec",
        invoice.invoice_number,
        time.perf_counter() - start
    )

    return new_invoice


@app.get("/invoices")
def get_invoices(
    db: Session = Depends(get_db)
):

    return db.query(Invoice).all()