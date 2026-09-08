# what does my data look like inside the databse? - used by database
from sqlalchemy import Column, Integer, String, Float, Date

from .database import Base

class Invoice(Base): 
    __tablename__ = "invoices" 

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
    ) 

    supplier = Column(
        String, 
        nullable=False
    ) 

    invoice_number = Column(
        String, 
        unique=True, 
        nullable = False
    )

    invoice_date = Column(
        Date, 
        nullable = False 
    )

    amount = Column(
        Integer, 
        nullable = False
    )

    currency = Column(
        String, 
        nullable = False
    )
