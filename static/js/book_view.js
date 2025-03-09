const readNowButton = document.getElementById("read-now-btn");
const coverContainer = document.getElementById("cover-container");
const readerContainer = document.getElementById("reader-container");
const pageContainer = document.getElementById("page-container");
const bookContent = document.getElementById("book_content").innerHTML; // Full book content
const tempContainer = document.getElementById("temp-container"); // Hidden container for measurement

const nextButton = document.getElementById("next-btn");
const prevButton = document.getElementById("prev-btn");
const pageInput = document.getElementById("page-number");
const totalPagesSpan = document.getElementById("total-pages");

let pages = [];
let currentPage = 0;

// Read Now Button Functionality
readNowButton.addEventListener("click", function () {
    coverContainer.classList.add("hidden");
    readerContainer.classList.remove("hidden");
    paginateContent(); // Initialize pagination when reading starts
});

// Function to paginate the content dynamically
function paginateContent() {
    pages = [];
    tempContainer.innerHTML = ""; // Clear previous content
    tempContainer.style.width = pageContainer.clientWidth + "px"; // Match book view width

    let content = document.createElement("div"); 
    content.innerHTML = bookContent; // Convert string to actual HTML elements

    let elements = content.childNodes; // Get all elements inside the book content
    let tempPage = document.createElement("div"); // Temporary container for one page

    for (let element of elements) {
        tempPage.appendChild(element.cloneNode(true)); // Clone element for this page
        tempContainer.innerHTML = tempPage.innerHTML; // Insert into temp container

        if (tempContainer.scrollHeight > pageContainer.clientHeight) {
            tempPage.removeChild(tempPage.lastChild); // Remove last element that overflows
            pages.push(tempPage.innerHTML); // Save this page
            tempPage = document.createElement("div"); // Start a new page
            tempPage.appendChild(element.cloneNode(true)); // Add the overflowed element to new page
        }
    }

    pages.push(tempPage.innerHTML); // Store the last page
    totalPagesSpan.textContent = `/ ${pages.length}`; // Update total pages
    displayPage(0);
}


// Function to display the selected page
function displayPage(index) {
    if (index >= 0 && index < pages.length) {
        pageContainer.innerHTML = pages[index]; // Load the page
        currentPage = index;
        pageInput.value = currentPage + 1;
        prevButton.disabled = currentPage === 0;
        nextButton.disabled = currentPage === pages.length - 1;
    }
}

// Event Listeners for Pagination Controls
nextButton.addEventListener("click", () => displayPage(currentPage + 1));
prevButton.addEventListener("click", () => displayPage(currentPage - 1));
pageInput.addEventListener("change", (event) => {
    let newPage = parseInt(event.target.value, 10) - 1;
    if (!isNaN(newPage) && newPage >= 0 && newPage < pages.length) {
        displayPage(newPage);
    }
});

// Recalculate pagination on window resize
window.addEventListener("resize", paginateContent);
