from web3 import Web3
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv()

provider_url = os.getenv("PROVIDER")
print('provider_url',provider_url)

# Conectando ao provedor
w3 = Web3(Web3.HTTPProvider(provider_url))
contract_address = os.getenv("CONTRACT_ADDRESS")

password = 'thlr rvze xgfc hhvb'

with open("abi.json", "r") as f:
    abi = f.read()

contract = w3.eth.contract(address=contract_address, abi=abi)

# Função para enviar email
def send_email(product_id, buyer,receiver_email):
    sender_email = "rmf.snf22@uea.edu.br"
    
    

    subject = f"Ingresso Festival Folclórico de Parintins"
    body = f"O número do seu ingresso é {product_id}, agradecemos a sua compra {buyer}, aproveite o festival."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)
        print("📩 E-mail enviado!")

# Monitorar eventos
def monitor_events():
    print("🔍 Monitorando eventos de venda...")
    # event_filter = contract.events.ProductPurchased.create_filter(fromBlock="latest")
    event_filter = w3.eth.filter({"address": contract_address})

    while True:
        for event in event_filter.get_new_entries():
            product_id = event["args"]["id"]
            buyer = event["args"]["buyer"]
            receiver_email = event["args"]["email"]
            send_email(product_id, buyer,receiver_email)
        time.sleep(10)



 
 
event_obj = contract.events.ProductPurchased()

filter_builder = event_obj.build_filter()
filter_builder.fromBlock = 'latest'
event_filter = filter_builder.deploy(w3)

print("🔔 Escutando eventos...")

while True:
    for event in event_filter.get_new_entries():
        print(f"✔ Produto comprado! ID: {event['args']['id']}, comprador: {event['args']['buyer']}, email: {event['args']['email']}")
        product_id = event["args"]["id"]
        buyer = event["args"]["buyer"]
        receiver_email = event["args"]["email"]
        send_email(product_id, buyer,receiver_email)
    time.sleep(10)

# if __name__ == "__main__":
    # monitor_events()
    # product_id=input('product_id')
    # buyer=input('buyer')
    # send_email(product_id, buyer)
