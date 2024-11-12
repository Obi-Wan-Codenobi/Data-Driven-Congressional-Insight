async function fetchPoliticians() {
    try {
        const response = await fetch('http://localhost:8000/api/politician/all');
        const data = await response.json();
        console.log('Fetched data:', data);
        createTable(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function createTable(data) {
    if (!Array.isArray(data)) {
        console.error('Data is not an array:', data);
        return;
    }

    const table = document.createElement('table');
    table.classList.add('politicians-table');

    const headerRow = document.createElement('tr');
    const headers = ['Image', 'Name', 'Party'];
    headers.forEach(headerText => {
        const header = document.createElement('th');
        header.textContent = headerText;
        headerRow.appendChild(header);
    });
    table.appendChild(headerRow);

    data.forEach(person => {
        const row = document.createElement('tr');

        const imgCell = document.createElement('td');
        const img = document.createElement('img');
        img.src = person.image_url;
        img.alt = person.name;
        img.width = 50;
        img.height = 50;
        imgCell.appendChild(img);
        row.appendChild(imgCell);

        const nameCell = document.createElement('td');
        nameCell.textContent = person.name;
        row.appendChild(nameCell);

        const partyCell = document.createElement('td');
        partyCell.textContent = person.party;
        row.appendChild(partyCell);

        table.appendChild(row);
    });

    document.getElementById('table-container').appendChild(table);
}

document.addEventListener('DOMContentLoaded', fetchPoliticians);
