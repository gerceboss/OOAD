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
    const recipientText = document.getElementById("recipientAddress");
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

      resultMessage.textContent = `Transaction sent! Payment successful`;
    } catch (error) {
      resultMessage.textContent = `Error: ${error.message}`;
    }
  });
});
