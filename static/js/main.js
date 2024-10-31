// Initialize Chart.js
let resultsChart = null;

function updateResultsTable(data) {
    const tableBody = document.getElementById('resultsTableBody');
    tableBody.innerHTML = '';
    
    Object.entries(data).forEach(([key, value]) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${key}</td>
            <td>${typeof value === 'number' ? value.toFixed(4) : value}</td>
        `;
        tableBody.appendChild(row);
    });
}

function updateVisualization(data) {
    const ctx = document.getElementById('resultsChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (resultsChart) {
        resultsChart.destroy();
    }
    
    // Create new chart
    resultsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                label: 'Results',
                data: Object.values(data),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
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

// Update the existing handleSubmit function
async function handleSubmit(event) {
    event.preventDefault();
    
    // ... existing form data collection ...

    try {
        const response = await fetch('/compute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        
        // Update the results display
        updateResultsTable(result);
        updateVisualization(result);
        
    } catch (error) {
        console.error('Error:', error);
        // Handle error appropriately
    }
} 