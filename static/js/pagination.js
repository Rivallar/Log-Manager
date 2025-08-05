// Shared pagination logic for all log pages
// Usage: Call updatePagination(...), updatePaginationInfo(...), and changePage(...) as needed

function updatePagination(currentResults, resultsPerPage, currentPage, onPageChange) {
    const totalPages = Math.ceil(currentResults.length / resultsPerPage);
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = '';
    if (totalPages <= 1) return;
    // Previous button
    const prevLi = document.createElement('li');
    prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
    prevLi.innerHTML = `<a class="page-link" href="#">Previous</a>`;
    prevLi.onclick = function(e) {
        e.preventDefault();
        if (currentPage > 1) onPageChange(currentPage - 1);
    };
    pagination.appendChild(prevLi);
    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
            const li = document.createElement('li');
            li.className = `page-item ${i === currentPage ? 'active' : ''}`;
            li.innerHTML = `<a class="page-link" href="#">${i}</a>`;
            li.onclick = function(e) {
                e.preventDefault();
                if (i !== currentPage) onPageChange(i);
            };
            pagination.appendChild(li);
        } else if (i === currentPage - 3 || i === currentPage + 3) {
            const li = document.createElement('li');
            li.className = 'page-item disabled';
            li.innerHTML = '<span class="page-link">...</span>';
            pagination.appendChild(li);
        }
    }
    // Next button
    const nextLi = document.createElement('li');
    nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
    nextLi.innerHTML = `<a class="page-link" href="#">Next</a>`;
    nextLi.onclick = function(e) {
        e.preventDefault();
        if (currentPage < totalPages) onPageChange(currentPage + 1);
    };
    pagination.appendChild(nextLi);
}

function updatePaginationInfo(currentResults, resultsPerPage, currentPage) {
    const startIndex = (currentPage - 1) * resultsPerPage + 1;
    const endIndex = Math.min(currentPage * resultsPerPage, currentResults.length);
    document.getElementById('showingStart').textContent = currentResults.length > 0 ? startIndex : 0;
    document.getElementById('showingEnd').textContent = endIndex;
    document.getElementById('totalResults').textContent = currentResults.length;
}