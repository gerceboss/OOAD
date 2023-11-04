// document.addEventListener("DOMContentLoaded", () => {
// //transfer amount
//     const Web3=require("web3");
//     const transferForm = document.getElementById("transferForm");
//     const transferButton = document.getElementById("transferButton");
//     const resultMessage = document.getElementById("resultMessage");

//     transferButton.addEventListener("click", async () => {
//         const senderAddress = document.getElementById("senderAddress").value;
//         const recipientAddress = document.getElementById("recipientAddress").value;
//         const amount = parseFloat(document.getElementById("amount").value);

//         // Initialize Web3.js and connect to an Ethereum node
//         const web3 = new Web3(new Web3.providers.HttpProvider("http://127.0.0.1:7545"));

//         // Send Ether from senderAddress to recipientAddress
//         try {
//             const gasPrice = await web3.eth.getGasPrice();
//             const transactionObject = {
//                 from: senderAddress,
//                 to: recipientAddress,
//                 value: web3.utils.toWei(amount.toString(), "ether"),
//                 gasPrice: gasPrice,
//             };
//             console.log("hello");
//             // Sign and send the transaction
//             const transactionHash = await web3.eth.sendTransaction(transactionObject);

//             resultMessage.textContent = `Transaction sent. Transaction hash: ${transactionHash}`;
//         } catch (error) {
//             resultMessage.textContent = `Error: ${error.message}`;
//         }
//     });
// });

document.addEventListener("DOMContentLoaded", () => {
  const transferForm = document.getElementById("transferForm");
  const transferButton = document.getElementById("transferButton");
  const resultMessage = document.getElementById("resultMessage");

  transferButton.addEventListener("click", async () => {
    const senderText = document.getElementById("senderAddress");
    console.log(senderText.innerHTML);
    const myArray1 = senderText.innerHTML.split(":");
    const senderAddress = myArray1[1];
    console.log(senderAddress);
    const recipientText = document.getElementById("senderAddress");
    const myArray2 = recipientText.innerHTML.split(":");
    const recipientAddress = myArray2[1];
    console.log(recipientAddress);
    const amountText = document.getElementById("amount");
    const myArray3 = amountText.innerHTML.split(":");
    const amount = parseFloat(myArray3[1]);
    console.log(typeof amount);

    if (typeof window.ethereum === "undefined") {
      resultMessage.textContent =
        "MetaMask is not installed. Please install it to use this feature.";
      return;
    }

    try {
      // Connect to MetaMask
      await ethereum.enable();

      // Initialize Web3.js
      const web3 = new Web3(window.ethereum);

      // Send Ether from senderAddress to recipientAddress
      const transaction = {
        from: senderAddress,
        to: recipientAddress,
        value: web3.utils.toWei(amount.toString(), "ether"),
      };

      const transactionHash = await web3.eth.sendTransaction(transaction);

      resultMessage.textContent = `Transaction sent. Transaction hash: ${transactionHash}`;
    } catch (error) {
      resultMessage.textContent = `Error: ${error.message}`;
    }
  });
});
