import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def extract_invoice(text: str):

    prompt = f"""
    You are an invoice information extraction system.

    Your task is to extract structured invoice information from the email below.

    IMPORTANT RULES:

    1. ONLY extract information that is actually present in the email.
    Do not invent, assume, or guess missing information.

    2. SUPPLIER:
    Extract the name of the company or organization issuing the invoice.

    3. INVOICE NUMBER:
    Extract the invoice number, reference number, or invoice ID.
    Do not confuse it with an order number, customer number, or account number.

    4. INVOICE DATE:
    Extract the date the invoice was issued.
    If the invoice date is not specified, return null.
    Do not use another date in the email as the invoice date.

    5. AMOUNT:
    Extract the total amount that needs to be paid.
    Do not confuse the total amount with individual line-item amounts,
    taxes, discounts, or other numbers mentioned in the email.

    6. CURRENCY:
    Always return the currency as a three-letter ISO 4217 currency code.

    Examples:
    € → EUR
    EUR → EUR
    £ → GBP
    GBP → GBP
    $ → USD
    USD → USD
    ¥ → JPY

    NEVER return currency symbols or additional text.
    For example, return "GBP", NOT "GBP (£)" or "£".

    7. DUE DATE:
    If the email provides a specific due date, extract it.

    Examples:
    "Payment by October 15th" → due_date = the specified date
    "Due on 30 September 2026" → due_date = 2026-09-30

    If the email does NOT provide a specific due date but gives a
    payment duration, extract the duration as due_days.

    Examples:
    "Payment within 30 days" → due_days = 30
    "Due in 14 days" → due_days = 14
    "Due in 1 week" → due_days = 7
    "Due in 1 month" → due_days = 30
    "Payment requested within 60 days" → due_days = 60

    If neither a specific due date nor a payment duration is provided,
    return both due_date and due_days as null.

    DO NOT calculate a due date yourself from a duration.
    Return the duration in due_days so that the application can
    calculate the date using today's date.

    8. DATES:
    Return dates in YYYY-MM-DD format.

    9. MISSING INFORMATION:
        If a field cannot be determined from the email, return null.
        Never make up a value.

    10. OUTPUT:
        Return ONLY the structured invoice information requested by the
        schema. Do not include explanations, comments, or additional text.
        The return should be a json type, but do NOT include the word "json"  
        OR any other additional words or phrases or marks. 

    EMAIL:

    {text}
    """

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=prompt,
    )

    return response.text