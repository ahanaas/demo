document.getElementById('analyze-button').addEventListener('click', function() {
    // Static data for demonstration
    const keywords = [
        { keyword: 'Machine Learning', frequency: 10 },
        { keyword: 'Gen AI', frequency: 9 },
        { keyword: 'Tensorflow', frequency: 8 },
        { keyword: 'News', frequency: 7 },
        { keyword: 'Data Analytics', frequency: 6 }
    ];

    const sentimentsData = {
        labels: ['Positive', 'Neutral', 'Negative'],
        datasets: [{
            label: 'Sentiment Analysis',
            data: [60, 30, 10],
            backgroundColor: [
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 99, 132, 0.2)'
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    };

    // Display keywords
    const keywordsText = keywords.map(k => `<span class="badge badge-primary">${k.keyword}</span>`).join(' ');
    document.getElementById('keywords-text').innerHTML = keywordsText;

    // Initialize Charts
    const ctxKeywords = document.getElementById('keywords-chart').getContext('2d');
    new Chart(ctxKeywords, {
        type: 'bar',
        data: {
            labels: keywords.map(k => k.keyword),
            datasets: [{
                label: 'Top 5 Keywords',
                data: keywords.map(k => k.frequency),
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
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

    const ctxSentiments = document.getElementById('sentiments-chart').getContext('2d');
    new Chart(ctxSentiments, {
        type: 'pie',
        data: sentimentsData,
        options: {
            responsive: true
        }
    });

    // Show results
    document.getElementById('results').classList.remove('hidden');
});
