// Function to fetch topics data from FastAPI server
async function fetchTopics() {
    try {
        const response = await fetch('http://localhost:8000/api/topics/all');
        const data = await response.json();
        console.log('Fetched data:', data);
        createTable(data);
        searchFunct(data);
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
    table.id = 'topics-table';

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

//Function filters the table using the search-bar
function searchFunct(data) {
    const bar = document.getElementById('search-bar');
    bar.addEventListener('input', event => {
        const query = event.target.value.toLowerCase();
        const table = document.getElementById('topics-table');
        const rows = table.querySelectorAll('tr:not(:first-child)');

        rows.forEach((row, index) => {
            const titleCell = row.querySelectorAll('td')[1];
            if (titleCell) {
                const title = titleCell.textContent.toLowerCase();
                if (title.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', fetchTopics);
