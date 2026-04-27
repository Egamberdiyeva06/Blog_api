import asyncio
import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = "durdonaegamberdiyeva36@gmail.com"
EMAIL_PASSWORD = "ybqx ywfu oodb buli"

async def send_welcome_email(email: str):
    msg = EmailMessage()
    msg['Subject'] = "Xush kelibsiz!"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content("Assalomu alaykum!\n\n"
        "Bizning xizmatimizdan ro'yxatdan o'tganingiz uchun rahmat. "
        "Sizni jamoamizda ko'rib turganimizdan xursandmiz!")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email muvaffaqiyatli yuborildi!")
    except Exception as e:
        print(f"Email yuborishda xato {email}: {e}")
