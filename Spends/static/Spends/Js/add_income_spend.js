document.getElementById('use-current-time').addEventListener('change', function() {
    if (this.checked) {
        const now = new Date().toISOString().split('T')[0];
        document.getElementById('income-date').value = now;
        document.getElementById('income-date').setAttribute('disabled', 'disabled');
    } else {
        document.getElementById('income-date').removeAttribute('disabled');
    }
});