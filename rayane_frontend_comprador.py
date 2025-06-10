import streamlit as st
from web3 import Web3
import json
import os
from dotenv import load_dotenv
import re
import warnings
warnings.filterwarnings("ignore")

def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

# Carrega variáveis do .env
load_dotenv()
private_key = os.getenv("PRIVATE_KEY_COMPRADOR") 

# Conexão Sepolia (Infura, Alchemy, etc.)
provider_url =  os.getenv("PROVIDER")
w3 = Web3(Web3.HTTPProvider(provider_url))
account = w3.eth.account.from_key(private_key)
sender_address = account.address

# Endereço do contrato Marketplace
contract_address = os.getenv("CONTRACT_ADDRESS")  

# ABI do contrato (resumida para os métodos principais)
with open("abi.json", "r") as f:
    abi = f.read()
contract = w3.eth.contract(address=contract_address, abi=json.loads(abi))

# ...imports e outras definições

# Mostra a imagem do cabeçalho
st.image("header.png", use_container_width=True)

st.title("🛒 Comprador")
st.markdown(f"Conectado como: `{sender_address}`")


# 📋 Listar Produtos
st.subheader("📋 Ingressos à Venda do Festival Folclórico de Parintins")
try:
    products = contract.functions.listProduct().call()
    for p in products:
         
        if(not p[4]):
            st.markdown(f"""
            #### 🛍️ Ingresso de número: {p[0]}
            - Preço: {w3.from_wei(p[1], 'ether')} ETH
            - Vendedor: `{p[2]}`
            - Torcida: **{p[7]}**
            - Tipo de Ingresso: **{p[5]}**			
            - Área do Ingresso: {p[6]}           
            """)
            email_key = f"email_{p[0]}"
            email_input = st.text_input("📧 Digite seu e-mail:", key=email_key)

            if email_input and not is_valid_email(email_input):
                st.warning("E-mail inválido. Verifique o formato, ex: nome@exemplo.com")
                
            if not p[4] and st.button(f"💰 Comprar Produto #{p[0]}"):
                try:
                    nonce = w3.eth.get_transaction_count(sender_address)
                    tx = contract.functions.purchaseProduct(p[0], email_input).build_transaction({
                        'chainId': 11155111,
                        'gas': 200000,
                        'gasPrice': w3.to_wei('10', 'gwei'),
                        'nonce': nonce,
                        'value': p[1]
                    })
                    signed = w3.eth.account.sign_transaction(tx, private_key)
                    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
                    st.success(f"Compra realizada! TX: {tx_hash.hex()}")
                except Exception as e:
                    st.error(str(e))
except Exception as e:
    st.error("Erro ao carregar produtos: " + str(e))

st.image("footer.png", use_container_width=True)
