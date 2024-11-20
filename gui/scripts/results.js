
async function searchDocuments(event, value, type) {
    event.preventDefault();
    let input;
    if (value && type) {
        input = value;
    }
    else {
        input = document.querySelector('.search-bar').value
    }

    if (input.trim() === '') {
        console.error('Search input is empty.');
        return;
    }

    const requestData = { input: input };

    try {
        const response = await fetch('http://localhost:8000/api/search/documents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();
        localStorage.setItem('searchResults', JSON.stringify(data));
        window.location.href = 'results.html';
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function displayResults() {
    const data = JSON.parse(localStorage.getItem('searchResults'));
    const tableContainer = document.getElementById('table-container');
    tableContainer.innerHTML = '';

    if (!data || !Array.isArray(data.json)) {
        console.error('Data is not an array or missing:', data);
        return;
    }

    const table = document.createElement('table');
    table.classList.add('results-table');

    const headerRow = document.createElement('tr');
    const headers = ['Title', 'Document'];
    headers.forEach(headerText => {
        const header = document.createElement('th');
        header.textContent = headerText;
        headerRow.appendChild(header);
    });
    table.appendChild(headerRow);

    data.json.forEach(doc => {
        const row = document.createElement('tr');

        const titleCell = document.createElement('td');
        titleCell.textContent = doc.title;
        row.appendChild(titleCell);

        const docCell = document.createElement('td');
        docCell.innerHTML = data.html_documents[doc.id];
        row.appendChild(docCell);

        table.appendChild(row);
    });

    tableContainer.appendChild(table);
}

function showLoadingAndRedirect() {
    document.getElementById('loading-screen').style.display = 'flex';
    setTimeout(() => { window.location.href = 'results.html'; }, 2000);
}
