document.addEventListener("DOMContentLoaded", function () {
    let textElement = document.getElementById("text");
    textElement.addEventListener("click", function (event) {
        let text = textElement.innerText;
        navigator.clipboard.writeText(text).then(() => {
            let popup = document.getElementById("popup");
            popup.style.left = event.pageX + "px";
            popup.style.top = event.pageY + "px";
            popup.style.opacity = 1;
            setTimeout(() => {
                popup.style.opacity = 0;
            }, 1000);
        }).catch(err => console.error("خطا در کپی:", err));
    });
});