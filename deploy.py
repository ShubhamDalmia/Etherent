import json
from web3 import Web3
from solcx import compile_standard, install_solc



with open("./PropertyRent.sol", "r") as file:
    rental_contract_file = file.read()

# Solidity source code
compiled_sol = compile_standard(
    {"language": "Solidity", "sources": {"PropertyRent.sol": {"content": rental_contract_file}}, "settings": {
        "outputSelection": {"*": {"*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]}}}, },
    solc_version="0.8.0", )

# We add these two lines that we forgot from the video!
print("Installing...")
install_solc("0.8.0")

# For connecting to ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
chain_id = 1337

my_address = "address"
private_key = "privatekey"

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["PropertyRent.sol"]["PropertyRent"]["evm"]["bytecode"]["object"]
# get abi
abi = json.loads(compiled_sol["contracts"]["PropertyRent.sol"]["PropertyRent"]["metadata"])["output"]["abi"]

# Create the contract in Python
PropertyRent = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# Submit the transaction that deploys the contract
transaction = PropertyRent.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send it!
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
# Wait for the transaction to be mined, and get the transaction receipt
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

def getNonce():
    nonce = w3.eth.getTransactionCount(my_address)
    return nonce


def addOwner(ownerWalletAddress, firstName, lastName, phoneNumber, balance):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    rental_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    addOwnerTransaction = rental_contract.functions.addOwner(
        ownerWalletAddress, firstName, lastName, phoneNumber, balance).buildTransaction(
        {"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": getNonce(), })

    signed_addOwner_Transaction = w3.eth.account.sign_transaction(addOwnerTransaction, private_key=private_key)
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_addOwner_Transaction.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print(rental_contract.functions.owners(ownerWalletAddress).call())

def addTenant(tenantWalletAddress, firstName, lastName, phoneNumber, rating, rentalPoints,canRent,lastRentPaid, dueAmount ):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    rental_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    addOwnerTransaction = rental_contract.functions.addTenant(
        tenantWalletAddress, firstName, lastName, phoneNumber, rating, rentalPoints,canRent,lastRentPaid, dueAmount).buildTransaction(
        {"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": getNonce(), })

    signed_addTenant_Transaction = w3.eth.account.sign_transaction(addOwnerTransaction, private_key=private_key)
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_addTenant_Transaction.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print(rental_contract.functions.tenants(tenantWalletAddress).call())


def addProperty(walletAddress, propertyId, currentlyRented, rent):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    rental_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    addOwnerTransaction = rental_contract.functions.addProperty(
        walletAddress, propertyId, currentlyRented, rent).buildTransaction(
        {"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": getNonce(), })

    signed_addProperty_Transaction = w3.eth.account.sign_transaction(addOwnerTransaction, private_key=private_key)
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_addProperty_Transaction.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print(rental_contract.functions.properties(propertyId).call())

def signAgreement(ownerWalletAddress,tenantWalletAddress,propertyId, start, end):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    rental_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    signgreementTransaction = rental_contract.functions.signAgreement(
        propertyId, start, end, ownerWalletAddress, tenantWalletAddress).buildTransaction(
        {"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": getNonce(), })

    signed_addOwner_Transaction = w3.eth.account.sign_transaction(signgreementTransaction, private_key=private_key)
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_addOwner_Transaction.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print(rental_contract.functions.propertyAgreementByPropertyId(propertyId).call())

def endAgreement(tenantWalletAddress,
                  propertyId, cleanlinessRating, neighbourRating):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    rental_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    endAgreementTransaction = rental_contract.functions.endAgreement(
        propertyId, tenantWalletAddress, cleanlinessRating, neighbourRating).buildTransaction(
        {"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": getNonce(), })

    signed_addOwner_Transaction = w3.eth.account.sign_transaction(endAgreementTransaction, private_key=private_key)
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_addOwner_Transaction.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print(rental_contract.functions.propertyAgreementByPropertyId(propertyId).call())

def makePayment(ownerWalletAddress,tenantWalletAddress):
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    rental_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    makePaymentTransaction = rental_contract.functions.makePayment(
        tenantWalletAddress, ownerWalletAddress).buildTransaction(
        {"chainId": chain_id, "gasPrice": w3.eth.gas_price, "from": my_address, "nonce": getNonce(), })

    signed_makePaymentTransaction = w3.eth.account.sign_transaction(makePaymentTransaction, private_key=private_key)
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_makePaymentTransaction.rawTransaction)
    print("Updating stored Value...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    print(rental_contract.functions.owners(ownerWalletAddress).call())

if __name__ == "__main__":
    addOwner("Address",
             "x",
             "y",
             "1234",
             0)

    addTenant("Address",
             "x",
             "y",
             "1234",
             0,0,True,0,0)

