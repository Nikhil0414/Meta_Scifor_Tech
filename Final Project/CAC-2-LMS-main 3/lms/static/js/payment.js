
  // Retrieve the amount from local storage and display in the input field
var storedAmount = localStorage.getItem("laundryAmount");
var amountInput = document.getElementById("amount");

if (storedAmount) {
    amountInput.value = storedAmount;
}

// Function to handle form submission


  