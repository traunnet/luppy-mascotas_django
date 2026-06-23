// Gráfico de dona — citas por estado
new Chart(document.getElementById('graficoCitas'), {
    type: 'doughnut',
    data: {
        labels: {{ grafico_citas.labels | safe }},
    datasets: [{
        data: {{ grafico_citas.valores | safe }},
    backgroundColor: ['#1976D2', '#2E7D32', '#C62828'],
    borderWidth: 2,
            }]
        },
    options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { position: 'bottom' }
    }
}
    });

// Gráfico de línea — ventas 7 días
new Chart(document.getElementById('graficoVentas'), {
    type: 'line',
    data: {
        labels: {{ labels_ventas|safe }},
        datasets: [{
            label: 'Ventas ($)',
            data: {{ valores_ventas|safe }},
            borderColor: '#2E7D32',
            backgroundColor: 'rgba(46,125,50,.15)',
            tension: .4,
            fill: true,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false }
        },
        scales: {
            y: { beginAtZero: true }
        }
    }
});