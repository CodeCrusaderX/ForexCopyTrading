# test_email.py
import yagmail

EMAIL = "prak1har@gmail.com"
PASSWORD = "xzsfcvtaqrfoxavg"

try:
    yag = yagmail.SMTP(EMAIL, PASSWORD)
    yag.send(
        to="keshavmelakhotia@gmail.com",
        subject="Test Email from Python",
        contents="This is a test email sent from a local script.",
        attachments=None  # You can add a dummy file to test PDF
    )
    print("✅ Email sent successfully!")
except Exception as e:
    print("❌ Error:", e)