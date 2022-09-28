function require(script) {
    $.ajax({
        url: script,
        dataType: "script",
        async: false,           // <-- This is the key
        success: function () {
            // all good...
        },
        error: function () {
            throw new Error("Could not load script " + script);
        }
    });
}

require("/static/pickpix/contract.js");

const container = document.getElementById("container");
var ethereum;
var accounts;
var currentTokenPrice;
var showingOwned = false;
var imageSize = 2050.0;
var maxCols = 224.0;

var chainIdName = {
    "0x1" : "Ethereum Main Network (Mainnet)",
    "0x3" : "Ropsten Test Network",
    "0x4" : "Rinkeby Test Network",
    "0x5" : "Goerli Test Network",
    "0x2a" : "Kovan Test Network",
    "0xa869" : "Avalanche FUJI C-Chain",
    "0xa86a" : "Avalanche Network"
}

function makeRows(rows, cols) {
    container.style.setProperty('--grid-rows', rows);
    container.style.setProperty('--grid-cols', cols);
    for (c = 0; c < (rows * cols); c++) {
        let cell = document.createElement("div");
        container.appendChild(cell).className = "grid-item";
    };
};

async function connectWallet() {
    if (typeof window.ethereum == 'undefined') {
        console.log('MetaMask is not installed.');
        return;
    }

    ethereum = window.ethereum;
    ethereum.on('accountsChanged', onAccountsUpdated);

    await init();
    //updateTokenPrice();
    //toggleOwnedTokens();
}

async function init() {
    updateTokenPrice();
    document.getElementById('contractAddress').textContent = "Contract Address: " + contractAddress;

    if (typeof ethereum == 'undefined' || !ethereum.isConnected()) {
        console.log('Web3 provider not installed or not connected');
        return;
    }

    updatedAccounts = await ethereum.request({ method: 'eth_requestAccounts' });
    onAccountsUpdated(updatedAccounts);
    toggleOwnedTokens();
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
    console.log("Accounts updated (all): " + accounts);
    chainName = getChainNameFromId(ethereum.chainId);
    var acct_trunc = accounts[0].slice(0, 6) + "..." + accounts[0].slice(-4);
    var details = chainName + " (" + acct_trunc + ")";
    document.getElementById('account').textContent = details;
}

async function requestVoucher() {
    var response;
    response = await $.get('/pickpix/voucher');
    console.log("response: " + response);
    return response;
}

async function getTokenPrice() {
    var response;
    response = await $.get('/pickpix/token_price');
    console.log("response: " + response.token_price);
    return response;
}

async function toggleOwnedTokens() {
//    if (showingOwned) {
//        var img_toggle = document.getElementById('show_owned_toggle');
        //img_toggle.src = '/static/pickpix/eye.png';
//        var markers = document.getElementsByClassName('token-marker');
//        for (i=0;i<markers.length;i++) {
//            markers[i].parentNode.removeChild(markers[i]);
//        }
//    } else if (accounts != null) {
    if (accounts != null) {
        var balance = await getOwnerBalance(accounts[0]);
        var img_toggle = document.getElementById('show_owned_toggle');
        var gridSize = imageSize / maxCols;
        // show the pixels
        tokens = await getTokensByOwner(accounts[0], balance);
        //console.log(tokens);
        pixels = await getPixelsByTokens(tokens);
        //console.log(pixels);
                var img = document.getElementById("secretImg");
        for (i = 0; i < pixels.length; i++) {
            var pixel = pixels[i];
            //var xCoord = (pixel % maxCols) * gridSize;
            //var yCoord = (pixel / maxCols) * gridSize;
            var col = (pixel % maxCols);
            var row = parseInt(pixel / maxCols);

            var tokenURI = await getTokenURI(tokens[i]);
            var arrow = document.createElement("div");
            arrow.style.width = gridSize*2+"px";
            arrow.style.height = gridSize*2+"px";
            arrow.style.left = (((col+1.1)/224) * 100)+"%";
            arrow.style.top = (((row+1.1)/224) * 100)+"%";
            arrow.style.position = "absolute";
            arrow.style.cursor = "pointer";
            arrow.classList.add("token-marker");
            arrow.setAttribute("onClick", "window.open('"+tokenURI+"')");
            img = document.createElement('img');
            img.src = '/static/pickpix/box_arrow.png';
            arrow.appendChild(img);
            container.appendChild(arrow);
        }

        //img_toggle.src = '/static/pickpix/eye_slash.png';
    }

    showingOwned = !showingOwned;
}

async function getTokenURI(tokenId) {
    let web3 = new Web3(ethereum);
    let contract = new web3.eth.Contract(contractABI, contractAddress);

    return await contract.methods.tokenURI(tokenId).call({});
}

async function getOwnerBalance(owner) {
    let web3 = new Web3(ethereum);
    let contract = new web3.eth.Contract(contractABI, contractAddress);

    return await contract.methods.balanceOf(accounts[0]).call({});
}

async function getTokenOfOwnerByIndex(owner, index) {
    let web3 = new Web3(ethereum);
    let contract = new web3.eth.Contract(contractABI, contractAddress);
    return await contract.methods.tokenOfOwnerByIndex(owner, index).call({});
}

async function getTokensByOwner(owner, balance) {
    var tokens = [];
    for (i = 0; i < balance; i++) {
        tokens.push(await getTokenOfOwnerByIndex(owner, i));
    }
    return tokens;
}

async function getPixelByToken(token) {
    let web3 = new Web3(ethereum);
    let contract = new web3.eth.Contract(contractABI, contractAddress);
    return await contract.methods.pixelIdFromTokenId(token).call({});
}

async function getPixelsByTokens(tokens) {
    var pixels = [];
    for (i = 0; i < tokens.length; i++) {
        pixels.push(await getPixelByToken(tokens[i]));
    }
    return pixels;
}

async function redeemToken() {
    if (typeof ethereum == 'undefined') {
        console.log("Wallet is not connected.");
        return;
    }
    if (accounts == null) {
        console.log("Wait for accounts to be updated")
    }

    let web3 = new Web3(ethereum);
    let contract = new web3.eth.Contract(contractABI, contractAddress);

    voucher = await requestVoucher();

    console.log(voucher.minPrice);
    console.log(voucher['signature']);
    voucher_tuple = [voucher.minPrice.toString(), voucher.uri, web3.utils.hexToBytes(voucher.signature)];

    contract.methods.redeem(accounts[0], voucher_tuple).send({from: accounts[0], value: voucher.minPrice})
    .on('transactionHash', function(hash) {
    })
    .on('confirmation', function(confirmationNumber, receipt) {
    })
    .on('receipt', function(receipt) {
        //console.log(receipt);
        tokenId = receipt.events.Transfer.returnValues["tokenId"];
        console.log("mintToken succeeded, token: " + tokenId);
        postToken(walletAddr, [tokenId]);
    })
    .on('error', function(error, receipt) {
        console.log("Transaction errored:");
        console.log(error);
        console.log(receipt);
    });
}

async function updateTokenPrice() {
    result = await getTokenPrice();

    document.getElementById('currentTokenPrice').textContent = "1 Pixel = " + result.token_price + " AVAX";
}

init();

/*window.addEventListener('load', () => {
        if (typeof web3 !== 'undefined') {
                connectWallet();
                toggleOwnedTokens();
        } else {
                console.log('No Web3 Detected... using HTTP Provider');
        }
});*/
