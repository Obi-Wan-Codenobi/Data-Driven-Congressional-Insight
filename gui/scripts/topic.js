// Function to fetch topics data from FastAPI server
async function fetchTopics() {
    try {
        const response = await fetch('http://localhost:8000/api/topics/all');  // Ensure the URL matches your endpoint
        const data = await response.json();
        console.log('Fetched data:', data);  // Log the data to check its structure
        createTable(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to create and display the table with topics data
function createTable(data) {
    if (!Array.isArray(data)) {
        console.error('Data is not an array:', data);
        return;
    }

    const table = document.createElement('table');
    table.classList.add('topics-table');

    const headerRow = document.createElement('tr');
    const headers = ['Image', 'Title'];
    headers.forEach(headerText => {
        const header = document.createElement('th');
        header.textContent = headerText;
        headerRow.appendChild(header);
    });
    table.appendChild(headerRow);

    data.forEach(topic => {
        const row = document.createElement('tr');

        const imgCell = document.createElement('td');
        const img = document.createElement('img');
        img.src = topic.image_url;
        img.alt = topic.title;
        img.width = 50;
        img.height = 50;
        imgCell.appendChild(img);
        row.appendChild(imgCell);

        const titleCell = document.createElement('td');
        titleCell.textContent = topic.title;
        row.appendChild(titleCell);

        table.appendChild(row);
    });

    document.getElementById('table-container').appendChild(table);
}

// Call the function when the DOM content is loaded
document.addEventListener('DOMContentLoaded', fetchTopics);
