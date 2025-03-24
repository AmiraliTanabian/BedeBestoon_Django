document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const submitBtn = document.querySelector(".submit-btn");
    const fields = form.querySelectorAll("input, textarea, select");

    // ذخیره مقدار اولیه فیلدها
    const initialValues = {};
    fields.forEach(field => {
        initialValues[field.name] = field.value;
    });

    function checkFormChanged() {
        let isChanged = false;

        fields.forEach(field => {
            if (initialValues[field.name] !== field.value) {
                isChanged = true;
            }
        });

        submitBtn.disabled = !isChanged; // دکمه را فعال/غیرفعال کن
    }

    // اضافه کردن event listener به همه فیلدها
    fields.forEach(field => {
        field.addEventListener("input", checkFormChanged);
        field.addEventListener("change", checkFormChanged);
    });
});
