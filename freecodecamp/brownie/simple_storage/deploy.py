from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

## Install Sol
version = "0.8.10"
install_solc(version)

## Open Contract
with open("./SimpleStorage.sol", "r") as file:
    contract_code = file.read()

inputJSON = {
    "language": "Solidity",
    "sources": {"SimpleStorage.sol": {"content": contract_code}},
    "settings": {
        "outputSelection": {
            "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
        }
    },
}
## Compile Contract
compiled_sol = compile_standard(inputJSON, solc_version=version)

with open("SimpleStorage.json", "w") as file:
    json.dump(compiled_sol, file, indent=4)

## Get bytecode and abi
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

## Connect to Ganache local netork
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/21e64ef539f84e63ba09c252ad433cc1")
)
chain_id = 4
address = os.getenv("TEST_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")

## Create Contract
SimpleStroage = w3.eth.contract(bytecode=bytecode, abi=abi)

nonce = w3.eth.getTransactionCount(address)
## Create Transaction for creating contract
transaction = SimpleStroage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": address,
        "nonce": nonce,
    }
)

## Sign Transaction
signed_transaction = w3.eth.account.signTransaction(transaction, private_key)

## Send Transaction
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_hash.hex())

## Interacting with Contract
contract_address = tx_receipt.contractAddress
simple_storage = w3.eth.contract(address=contract_address, abi=abi)
store_transaction = simple_storage.functions.store(42).buildTransaction(
    {
        "chainId": chain_id,
        "from": address,
        "nonce": nonce + 1,
    }
)

signed_store_transaction = w3.eth.account.signTransaction(store_transaction, private_key)

tx_hash = w3.eth.sendRawTransaction(signed_store_transaction.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_hash.hex())

print(simple_storage.functions.retrieve().call())
