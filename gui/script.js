document.addEventListener("DOMContentLoaded", () => {
    console.log("GUI is loaded!");
});

function showLoadingAndRedirect() {
    document.getElementById('loading-screen').style.display = 'flex';
    setTimeout(() => { window.location.href = 'results.html'; }, 2000);
}




/*Results Page Functions*/

document.addEventListener('DOMContentLoaded', displayDocuments);


const documents = [
    { title: "Document 1", date: "2024-01-01", link: "doc1.html" },
    { title: "Document 2", date: "2024-02-01", link: "doc2.html" },
    { title: "Document 3", date: "2024-03-01", link: "doc3.html" },
    { title: "Document 4", date: "2024-04-01", link: "doc4.html" },
    { title: "Document 5", date: "2024-05-01", link: "doc5.html" }
];


function displayDocuments() {
    const documentList = document.getElementById('document-list');
    if (documentList) {
        documents.forEach(doc => {

            const docContainer = document.createElement('div');
            docContainer.classList.add('document-container');


            const docLink = document.createElement('a');
            docLink.href = doc.link;
            docLink.textContent = `${doc.title} - ${doc.date}`;
            docLink.classList.add('document-link');


            docContainer.appendChild(docLink);


            documentList.appendChild(docContainer);
        });
    } else {
        console.error('document-list element not found');
    }
}

