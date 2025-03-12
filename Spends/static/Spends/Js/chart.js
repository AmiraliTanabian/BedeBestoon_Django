document.addEventListener("DOMContentLoaded", function() {
    const ctx = document.getElementById("expense-income-chart").getContext("2d");

    const expenseData = [2, 34, 5, 6];
    const incomeData = [6, 8, 10];
    const labels = ["فروردین", "اردیبهشت", "خرداد", "تیر"]; // نمونه ماه‌ها

    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "هزینه‌ها",
                    data: expenseData,
                    borderColor: "red",
                    backgroundColor: "rgba(255, 0, 0, 0.2)",
                    fill: true
                },
                {
                    label: "درآمدها",
                    data: incomeData,
                    borderColor: "green",
                    backgroundColor: "rgba(0, 255, 0, 0.2)",
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
});