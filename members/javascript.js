const Web3 = require("web3");
async function transfer(addr1, addr2, amount) {
  if (typeof window.ethereum === "undefined") {
    // resultMessage.textContent =
    //   "MetaMask is not installed. Please install it to use this feature.";
    // return;
    console.log("no metamask");
    return;
  }
  try {
    // Connect to MetaMask
    await ethereum.enable();

    // Initialize Web3.js
    const web3 = new Web3(window.ethereum);

    // Send Ether from senderAddress to recipientAddress
    const transaction = {
      from: addr1,
      to: addr2,
      value: web3.utils.toWei(amount.toString(), "ether"),
    };

    const transactionHash = await web3.eth.sendTransaction(transaction);
    console.log(transactionHash);
    //resultMessage.textContent = `Transaction sent. Transaction hash: ${transactionHash}`;
  } catch (error) {
    console.log("error");
    //resultMessage.textContent = `Error: ${error.message}`;
  }
}
