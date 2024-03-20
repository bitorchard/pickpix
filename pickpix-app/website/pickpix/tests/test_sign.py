from web3 import Web3
from eth_account.messages import encode_structured_data
from struct import *
import json

PROVIDER_URL = "https://api.avax-test.network/ext/bc/C/rpc"
CONTRACT_JSON_FILE = "contract.json"

PRIVATE_KEY = "0xe607298786fc31a8606539101856730258f0192f757664ca7198902e1d3ac713"

w3 = Web3(Web3.HTTPProvider(PROVIDER_URL))

with open(CONTRACT_JSON_FILE) as f:
    contract_json = json.load(f)

data = {
    "types" : {
        "EIP712Domain": [
            { "name": "name", "type": "string" },
#            { "name": "version", "type": "string" },
            { "name": "chainId", "type": "uint256" },
         #   { "name": "verifyingContract", "type": "address" },
        ],
        "NFTVoucher" : [
            { "name": "minPrice", "type": "uint256" },
            { "name": "uri", "type": "string" },
        ],
    },
    #"domain" : {},
    "domain" : {
        "name": "Pixel-Voucher",
        "chainId": 43113,
        #"verifyingContract": "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
    #    "version": "1",
    },
    "primaryType": "NFTVoucher",
    "message" : {
        "minPrice" : 100,
        "uri" : "TESTURI",
    }
}

#encoded_data = encode_structured_data(data)
#signature = w3.eth.signTypedData(w3.eth.defaultAccount, encoded_data)

signable = encode_structured_data(data)
signed = w3.eth.account.sign_message(signable, PRIVATE_KEY)

print(signable)
print(signed.signature.hex())
