setTimeout(function() {
    var errorBox = document.getElementById("error-message");
    if (errorBox) {
        errorBox.style.opacity = "0";
        setTimeout(() => errorBox.remove(), 500);
    }
}, 3000);
