t contractAddress = '0xff3a3df1443a5d8be57ff9041a477a3853b96ae2';
const contractABI = [ { "inputs": [], "stateMutability": "nonpayable", "type": "constructor" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "owner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "approved", "type": "address" }, { "indexed": true, "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "Approval", "type": "event" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "owner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "operator", "type": "address" }, { "indexed": false, "internalType": "bool", "name": "approved", "type": "bool" } ], "name": "ApprovalForAll", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "approve", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "decimals", "outputs": [ { "internalType": "uint8", "name": "", "type": "uint8" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [], "name": "magicNumber", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "recipient", "type": "address" } ], "name": "mintToken", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "nonpayable", "type": "function" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "previousOwner", "type": "address" }, { "indexed": true, "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "OwnershipTransferred", "type": "event" }, { "inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "from", "type": "address" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "safeTransferFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "from", "type": "address" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" }, { "internalType": "bytes", "name": "_data", "type": "bytes" } ], "name": "safeTransferFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "operator", "type": "address" }, { "internalType": "bool", "name": "approved", "type": "bool" } ], "name": "setApprovalForAll", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "anonymous": false, "inputs": [ { "indexed": true, "internalType": "address", "name": "from", "type": "address" }, { "indexed": true, "internalType": "address", "name": "to", "type": "address" }, { "indexed": true, "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "Transfer", "type": "event" }, { "inputs": [ { "internalType": "address", "name": "from", "type": "address" }, { "internalType": "address", "name": "to", "type": "address" }, { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "transferFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "newOwner", "type": "address" } ], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "owner", "type": "address" } ], "name": "balanceOf", "outputs": [ { "internalType": "uint256", "name": "", "type": "uint256" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "getApproved", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "address", "name": "owner", "type": "address" }, { "internalType": "address", "name": "operator", "type": "address" } ], "name": "isApprovedForAll", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "name", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "owner", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "ownerOf", "outputs": [ { "internalType": "address", "name": "", "type": "address" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "bytes4", "name": "interfaceId", "type": "bytes4" } ], "name": "supportsInterface", "outputs": [ { "internalType": "bool", "name": "", "type": "bool" } ], "stateMutability": "view", "type": "function" }, { "inputs": [], "name": "symbol", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" }, { "inputs": [ { "internalType": "uint256", "name": "tokenId", "type": "uint256" } ], "name": "tokenURI", "outputs": [ { "internalType": "string", "name": "", "type": "string" } ], "stateMutability": "view", "type": "function" } ];
walletAddr = '0xa5A400D0096AFD66438139c52072dd89306D8da5';

const container = document.getElementById("container");
var ethereum;
var accounts;

var chainIdName = {
    "0x1" : "Ethereum Main Network (Mainnet)",
    "0x3" : "Ropsten Test Network",
    "0x4" : "Rinkeby Test Network",
    "0x5" : "Goerli Test Network",
    "0x2a" : "Kovan Test Network",
    "0xa869" : "Avalanche FUJI C-Chain"
}

function makeRows(rows, cols) {
    container.style.setProperty('--grid-rows', rows);
    container.style.setProperty('--grid-cols', cols);
    for (c = 0; c < (rows * cols); c++) {
        let cell = document.createElement("div");
        cell.innerText = (c + 1);
        if (usedPixels.includes(c)) {
            cell.style.backgroundColor = "#00FF00";
        }
        container.appendChild(cell).className = "grid-item";
    };
};

function connectWallet() {
    if (typeof window.ethereum == 'undefined') {
        console.log('MetaMask is not installed.');
        return;
    }

    ethereum = window.ethereum;
    ethereum.on('accountsChanged', onAccountsUpdated);

    init();
    updateMagicNumber();
}

async function init() {
    if (typeof ethereum == 'undefined' || !ethereum.isConnected()) {
        return;
    }

    updatedAccounts = await ethereum.request({ method: 'eth_requestAccounts' });
    onAccountsUpdated(updatedAccounts);
}

function getChainNameFromId(id) {
    name = chainIdName[id];
    if (typeof id == 'undefined') {
        name = "None";
    }
    return name;
}

function onAccountsUpdated(updatedAccounts) {
    accounts = updatedAccounts;
    console.log("Accounts updated: " + accounts[0]);
    chainName = getChainNameFromId(ethereum.chainId);
    details = chainName + " (" + accounts[0] + ")";
    document.getElementById('account').textContent = details;
}

function mintToken() {
    if (typeof ethereum == 'undefined') {
        console.log("Wallet is not connected.");
        return;
    }

    let web3 = new Web3(ethereum);
    let contract = new web3.eth.Contract(contractABI, contractAddress);

    contract.methods.mintToken(walletAddr).send({from: walletAddr})
    .on('transactionHash', function(hash) {
        //console.log(hash);
    })
    .on('confirmation', function(confirmationNumber, receipt) {
        //console.log(confirmationNumber);
        //console.log(receipt);
    })
    .on('receipt', function(receipt) {
        //console.log(receipt);
        tokenId = receipt.events.Transfer.returnValues["tokenId"];
        console.log("mintToken succeeded, token: " + tokenId);
        postToken(walletAddr, tokenId);
    })
    .on('error', function(error, receipt) {
        console.log("Transaction errored:");
        console.log(error);
        console.log(receipt);
    });
}

function postToken(owner, tokenId) {
    var http;

    if (!window.XMLHttpRequest) {
        console.log("Need browser support for window.XMLHttpRequest?");
        return;
    }

    http = new XMLHttpRequest();
    http.open("POST", "/pickpix/token/", true);
    http.setRequestHeader("Accept", "application/json");
    http.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

    http.send(JSON.stringify({'owner' : owner, 'tokenId' : tokenId}));
}

function updateMagicNumber() {
    if (typeof ethereum == 'undefined') {
        console.log("Wallet is not connected.");
        return;
    }

    let web3 = new Web3(ethereum);
    let contract = new web3.eth.Contract(contractABI, contractAddress);

    contract.methods.magicNumber().call({from: walletAddr})
    .then(function(result) {
        console.log("Got the magic number: " + result);
        document.getElementById('magicNumber').textContent = result;
    });
}

//init();
makeRows(50, 50);
