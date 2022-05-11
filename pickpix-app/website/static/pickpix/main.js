const contractAddress = '1e37275f7058a374c8a35b74df7acf070c660336';
const contractABI = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"magicNumber","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"}],"name":"mintToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}];

const container = document.getElementById("container");
var hydraweb3;
var hydraAccount;

function makeRows(rows, cols) {
    container.style.setProperty('--grid-rows', rows);
    container.style.setProperty('--grid-cols', cols);
    for (c = 0; c < (rows * cols); c++) {
        let cell = document.createElement("div");
        cell.innerText = (c + 1);
        container.appendChild(cell).className = "grid-item";
  };
};

function initHydraWallet() {
    if (typeof window.hydrawallet == 'undefined') {
        window.postMessage({ message: { type: 'CONNECT_HYDRAWALLET' } }, '*');
    }
}

async function updateWallet() {
    //initHydraWallet();

    if (typeof hydraAccount == 'undefined' || !hydraAccount.loggedIn) {
        console.log("Hydra account not logged in");
        return;
    }

    var contract = hydraweb3.Contract(contractAddress, contractABI);

    var steveAddr = 'Tmu5zsGtqdkKBDwk7uuApkj13rYgQnN1KS';

    var methodName = 'magicNumber';

    /*callResult = await contract.call('balanceOf', {
        methodArgs: [steveAddr],
        senderAddress: steveAddr,
    });*/
    console.log("Call contract: " + contractAddress + " (" + methodName + ")");

	callResult = await contract.call(methodName, {
		methodArgs: [],
		senderAddress: steveAddr,
	});

    decode = hydraweb3.decoder.decodeCall(callResult, contractABI, methodName, true);
    //decode = hydraweb3.decoder.decodeCall(callResult, contractABI, 'balanceOf', true);
	fmtOutput = decode.executionResult.formattedOutput;

    var magicNumber;
        //for (var key in fmtOutput.executionResult.formattedOutput) {
	for (var key in fmtOutput) {
        console.log(methodName + " result: " + fmtOutput[key]);
        magicNumber = fmtOutput[key];
        const mnSpan = document.getElementById('magicNumber');
        mnSpan.textContent = magicNumber;
    }
    //console.log("callResult: " + fmtOutput.executionResult.formattedOutput);
}

function onHydrawalletAccountChange(event) {
	if (event.data.message && event.data.message.type == "HYDRAWALLET_ACCOUNT_CHANGED") {
		hydraAccount = event.data.message.payload.account;
		console.log("hydraAccount: " + hydraAccount.name + " (" + hydraAccount.network + ")");
		hydraweb3 = new Hydraweb3(window.hydrawallet.rpcProvider);
		//updateWallet();
		const status = document.getElementById('walletStatus');
		status.textContent = hydraAccount.loggedIn.toString();
	}
}

initHydraWallet();
window.addEventListener('message', onHydrawalletAccountChange, false);

makeRows(50, 50);
