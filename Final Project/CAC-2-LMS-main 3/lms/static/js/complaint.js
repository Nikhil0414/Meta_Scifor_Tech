function submitNewComplaint() {
    const orderId = document.getElementById('orderIdInput').value;
    const user = document.getElementById('userInput').value;
    const complaint = document.getElementById('complaintInput').value;
  
    if (orderId && user && complaint) {
      // Show pop-up with success message
      showPopup('Complaint received successfully! Thank you for your feedback.', 'success');
    } else {
      // Show pop-up with error message
      showPopup('All fields are mandatory. Please fill in all fields.', 'error');
    }
  }
  
  function showPopup(message, type) {
    const popupContainer = document.getElementById('popupContainer');
    const popupMessage = document.getElementById('popupMessage');
  
    // Set the message content and style
    popupMessage.innerHTML = message;
    popupContainer.className = `popup-container active ${type}`;
  
    // Hide the pop-up container after 3 seconds (adjust as needed)
    setTimeout(() => {
      popupContainer.classList.remove('active', type);
    }, 5000);
  }
  