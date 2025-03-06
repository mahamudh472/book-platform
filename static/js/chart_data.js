function render_chart(chartId, labels_array, data_array, label) {
    const ctx = document.getElementById(chartId).getContext('2d');

    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels_array,
            datasets: [{
                label: label,
                data: data_array,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}