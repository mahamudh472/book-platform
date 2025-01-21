
// Get the context of the canvas
const ctx = document.getElementById('myChart').getContext('2d');

// Create the chart
const myChart = new Chart(ctx, {
    type: 'line', // Chart type: bar, line, pie, doughnut, etc.
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Augest', 'September', 'October', 'November', 'December'], // X-axis labels
        datasets: [{
            label: 'Views', // Chart legend
            data: [10, 20, 5, 7, 9, 8, 0, 20, 19, 6, 12, 5], // Data points
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1 // Border width for the bars
        }]
    },
    options: {
        responsive: true, // Makes the chart responsive
        scales: {
            y: {
                beginAtZero: true // Starts y-axis at zero
            }
        }
    }
});