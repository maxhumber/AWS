from email.message import EmailMessage
import os
import smtplib
from dotenv import find_dotenv, load_dotenv
from gazpacho import get, Soup

load_dotenv(".env")

sender = os.environ.get("GMAIL_USER")
password = os.environ.get("GMAIL_PASSWORD")
recipient = os.environ.get("RECIPIENT_EMAIL")

def parse(book):
    name = book.find("h4").text
    price = float(book.find("p").text[1:].split(" ")[0])
    return name, price

def fetch_sale():
    url = "https://scrape.world/books"
    html = get(url)
    soup = Soup(html)
    books_raw = soup.find("div", {"class": "book-"})
    books = [parse(book) for book in books_raw]
    on_sale = [name for name, price in books if price == 0.99]
    return "\n".join(on_sale)

def send_email(sender, password):
    on_sale = fetch_sale()
    if on_sale:
        body = f"These books are on sale:\n{on_sale}\n\nBuy them now!"
    else:
        body = "Nothing on sale :("
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = "Books Bot"
    msg["From"] = sender
    msg["To"] = recipient
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    # https://support.google.com/accounts/answer/185833
    send_email(sender, password)
