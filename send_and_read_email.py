import smtplib
import imaplib
import email
from email.mime.text import MIMEText

# Đọc thông tin tài khoản từ file
with open('email_credentials.txt', 'r') as file:
    account_info = file.readlines()
    sender_email = account_info[0].strip()
    app_password = account_info[1].strip()

# Đọc nội dung email, người nhận, tiêu chí lọc
with open('email_content.txt', 'r') as file:
    email_content = file.read()

with open('recipient.txt', 'r') as file:
    recipient_email = file.read().strip()

with open('email_filter.txt', 'r') as file:
    filter_sender = file.read().strip()

# Gửi email
msg = MIMEText(email_content)
msg['Subject'] = 'Email Tự Động'
msg['From'] = sender_email
msg['To'] = recipient_email

try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)
        print("Email đã gửi thành công!")
except Exception as e:
    print(f"Lỗi khi gửi email: {e}")

# Đọc email
try:
    with imaplib.IMAP4_SSL('imap.gmail.com') as mail:
        mail.login(sender_email, app_password)
        mail.select('INBOX')
        _, data = mail.search(None, f'FROM "{filter_sender}"')
        for num in data[0].split():
            _, msg_data = mail.fetch(num, '(RFC822)')
            email_msg = email.message_from_bytes(msg_data[0][1])
            subject = email_msg['subject']
            print(f"Tiêu đề email nhận được: {subject}")
            if email_msg.is_multipart():
                for part in email_msg.walk():
                    if part.get_content_type() == 'text/plain':
                        print(f"Nội dung:\n{part.get_payload(decode=True).decode()}")
            else:
                print(f"Nội dung:\n{email_msg.get_payload(decode=True).decode()}")
            break  # Xử lý 1 email đầu tiên là đủ
except Exception as e:
    print(f"Lỗi khi nhận email: {e}")
