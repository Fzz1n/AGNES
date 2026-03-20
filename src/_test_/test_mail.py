from src.mail import send_email

def test_send_email():
    title = "Title crerate by test"
    body = "This is a test email sent from Python."
    res = send_email(title, body)
    assert res == "Email send"