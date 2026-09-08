# What data am I allowed to send and recieve throuhg my API - used by API 
from pydantic import BaseModel, field_validator
from datetime import date 

class InvoiceCreate(BaseModel):
    supplier:str 
    invoice_number:str 
    invoice_date:date 
    amount:float 
    currency:str

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value): 

        allowed = {"EUR","USD","GBP"}

        if value not in allowed: 
            raise ValueError("Unsupported currency")

        return value 

    @field_validator("invoice_date")
    @classmethod
    def validate_invoice_date(cls, value): 

        if value > date.today(): 

            raise ValueError("Invoice date cannot be in the future") 

        return value