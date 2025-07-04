import yagmail
import streamlit as st

def send_pdf_email(recipient, subject, body, attachment_path):
    try:
        st.write("📤 Attempting to send email...")
        st.write(f"From: {st.secrets['EMAIL']}")
        st.write(f"To: {recipient}")
        st.write(f"Attaching: {attachment_path}")
        
        yag = yagmail.SMTP(user=st.secrets["EMAIL"], password=st.secrets["EMAIL_PASSWORD"])
        yag.send(
            to=recipient,
            subject=subject,
            contents=body,
            attachments=attachment_path
        )
        st.success("✅ Email sent successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
        return False