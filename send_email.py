# import yagmail
# import streamlit as st

# def send_pdf_email(recipient, subject, body, attachment_path):
#     try:
#         yag = yagmail.SMTP(user=st.secrets["EMAIL"], password=st.secrets["EMAIL_PASSWORD"])
#         yag.send(
#             to=recipient,
#             subject=subject,
#             contents=body,
#             attachments=attachment_path
#         )
#         return True
#     except Exception as e:
#         st.error(f"Failed to send email: {e}")
#         return False
import yagmail
import streamlit as st

def send_pdf_email(recipient, subject, body, attachment_path):
    try:
        st.write("📨 Connecting to SMTP...")
        yag = yagmail.SMTP(user=st.secrets["EMAIL"], password=st.secrets["EMAIL_PASSWORD"])
        st.write("✅ SMTP connected. Sending...")
        yag.send(
            to=recipient,
            subject=subject,
            contents=body,
            attachments=attachment_path
        )
        st.write("✅ Email sent.")
        return True
    except Exception as e:
        st.error(f"❌ Email failed: {e}")
        return False