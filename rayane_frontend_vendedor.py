import streamlit as st
from web3 import Web3
import json
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
private_key = os.getenv("PRIVATE_KEY_VENDEDOR")

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

st.title("🛒 Vendedor")
st.markdown(f"Conectado como: `{sender_address}`")

# ✅ Adicionar Produto
st.subheader("Cadastrar Ingresso do Festival Folclórico de Parintins")
 
torcida = st.selectbox(
    "Torcida",
    ["Garantido", "Caprichoso"]
)

ticket_type = st.selectbox(
    "Tipo do ingresso",
    ["Inteira", "Meia", "VIP", "Cortesia"]
)

ticket_area = st.selectbox(
    "Área do ingresso",
    ["Pista ", "Camarote", "Arquibancada", "Área Premium"]
)

 

 



price_eth = st.number_input("Preço (em ETH)", min_value=0.0001, format="%.4f")
price_wei = w3.to_wei(price_eth, 'ether')

if st.button("📤 Adicionar"):
    try:
        nonce = w3.eth.get_transaction_count(sender_address)
        tx = contract.functions.addProduct( price_wei, ticket_type, ticket_area, torcida).build_transaction({
            'chainId': 11155111,
            'gas': 300000,
            'gasPrice': w3.to_wei('10', 'gwei'),
            'nonce': nonce
        })
        signed = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        st.success(f"Produto enviado! TX: {tx_hash.hex()}")
    except Exception as e:
        st.error(str(e))


# 📋 Listar Produtos
st.subheader("📋 Ingressos à Venda")
try:
    products = contract.functions.listProduct().call()
    for p in products:
        st.markdown(f"""
        #### 🛍️ Ingresso de número: {p[0]}
        - Preço: {w3.from_wei(p[1], 'ether')} ETH
        - Vendedor: `{p[2]}`
        - Vendido: {"✅ Sim" if p[4] else "❌ Não"}
        - Torcida: **{p[7]}**       
        - Tipo de Ingresso: **{p[5]}**
        - Área do Ingresso: {p[6]}
        """)
except Exception as e:
    st.error("Erro ao carregar produtos: " + str(e))

except Exception as e:
    st.error("Erro ao carregar produtos: " + str(e))

