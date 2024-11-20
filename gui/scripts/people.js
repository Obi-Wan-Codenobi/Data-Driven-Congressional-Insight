import { searchDocuments, showLoadingAndRedirect } from './results.js'

//Function to call the other funcitons when loaded
async function fetchPoliticians() {
    showLoading();
    try {
        const response = await fetch('http://localhost:8000/api/politician/all');
        const data = await response.json();
        console.log('Fetched data:', data);
        createTable(data);
        searchFunct(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    } finally {
        hideLoading();
    }
}

//Function to create table of politians
function createTable(data) {
    if (!Array.isArray(data)) {
        console.error('Data is not an array:', data);
        return;
    }

    const table = document.createElement('table');
    table.classList.add('politicians-table');
    table.id = 'politicians-table';
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

        row.addEventListener('click', () => {
            handleRowClick(person);
        });
        table.appendChild(row);
    });

    document.getElementById('table-container').appendChild(table);
}


//handling clicks
function handleRowClick(person) {
    const event = new Event('click');
    searchDocuments(event, person.name, 'people');
    showLoadingAndRedirect();
}

//Function to filter the polititian table
function searchFunct(data) {
    const bar = document.getElementById('search-bar');
    bar.addEventListener('input', event => {
        const query = event.target.value.toLowerCase();
        const table = document.getElementById('politicians-table');
        const rows = table.querySelectorAll('tr:not(:first-child)');

        rows.forEach((row, index) => {
            const nameCell = row.querySelectorAll('td')[1];
            if (nameCell) {
                const name = nameCell.textContent.toLowerCase();
                if (name.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            }
        });
    });
}
document.addEventListener('DOMContentLoaded', fetchPoliticians);

function showLoading() {
    document.getElementById('loading-screen').style.display = 'flex';
}
function hideLoading() {
    document.getElementById('loading-screen').style.display = 'none';
}
