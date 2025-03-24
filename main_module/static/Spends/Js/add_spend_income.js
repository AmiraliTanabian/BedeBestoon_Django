document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('id_is_now').addEventListener('change', function() {
        if (this.checked) {
            document.getElementById('id_datetime').setAttribute('disabled', 'disabled');
        } else {
            document.getElementById('id_datetime').removeAttribute('disabled');
        }
    });
});