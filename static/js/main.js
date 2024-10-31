// Initialize Chart.js
let resultsChart = null;

// Error messages
const ERROR_MESSAGES = {
    TABLE_NOT_FOUND: 'Results table body element not found',
    CHART_NOT_FOUND: 'Results chart canvas element not found',
    API_ERROR: 'Error communicating with server'
};

/**
 * Updates the results table with the provided data
 * @param {Object} data - The data to display in the table
 * @throws {Error} If table body element is not found
 */
function updateResultsTable(data) {
    const tableBody = document.getElementById('resultsTableBody');
    if (!tableBody) {
        throw new Error(ERROR_MESSAGES.TABLE_NOT_FOUND);
    }
    
    tableBody.innerHTML = '';
    
    Object.entries(data).forEach(([key, value]) => {
        const row = document.createElement('tr');
        const formattedValue = typeof value === 'number' ? 
            Number(value).toFixed(4) : 
            String(value);
            
        row.innerHTML = `
            <td>${escapeHtml(key)}</td>
            <td>${escapeHtml(formattedValue)}</td>
        `;
        tableBody.appendChild(row);
    });
}

/**
 * Escapes HTML special characters to prevent XSS
 * @param {string} unsafe - String to escape
 * @returns {string} Escaped string
 */
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/**
 * Updates the visualization chart with the provided data
 * @param {Object} data - The data to visualize
 * @throws {Error} If chart canvas element is not found
 */
function updateVisualization(data) {
    const canvas = document.getElementById('resultsChart');
    if (!canvas) {
        throw new Error(ERROR_MESSAGES.CHART_NOT_FOUND);
    }
    
    const ctx = canvas.getContext('2d');
    
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
                label: 'Simulation Results',
                data: Object.values(data),
                backgroundColor: 'rgba(54, 162, 235, 0.5)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => Number(value).toFixed(2)
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: context => `Value: ${Number(context.raw).toFixed(4)}`
                    }
                }
            }
        }
    });
}

/**
 * Handles form submission and updates results
 * @param {Event} event - The submit event
 */
async function handleSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = {
        participantCount: parseInt(form.querySelector('#participantCount').value, 10)
    };

    try {
        const response = await fetch('/api/simulate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        
        // Update the results display
        updateResultsTable(result);
        updateVisualization(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert(ERROR_MESSAGES.API_ERROR);
    }
}

// Add event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#simulationForm');
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
});