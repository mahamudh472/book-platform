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

readNowButton.addEventListener("click", function () {
    coverContainer.classList.add("hidden");
    readerContainer.classList.remove("hidden");

    // Wait for styles to fully apply before paginating
    requestAnimationFrame(() => {
        paginateContent();
    });
});





function paginateContent() {
    pages = [];
    tempContainer.innerHTML = ""; // Clear previous content
    tempContainer.style.width = pageContainer.clientWidth + "px"; // Match width
    tempContainer.style.position = "absolute"; // Prevent layout shifting
    tempContainer.style.visibility = "hidden"; // Hide from view
    document.body.appendChild(tempContainer); // Append for measurement

    // 🔥 Get padding values dynamically
    const computedStyle = window.getComputedStyle(pageContainer);
    const paddingTop = parseFloat(computedStyle.paddingTop);
    const paddingBottom = parseFloat(computedStyle.paddingBottom);
    const lineHeight = parseFloat(computedStyle.lineHeight) || 24; // Default fallback
    const extraMargin = 8; // Additional buffer space

    const availableHeight = pageContainer.clientHeight - (paddingTop + paddingBottom + extraMargin);

    let content = document.createElement("div");
    content.innerHTML = bookContent; // Convert string to actual HTML elements
    let elements = Array.from(content.childNodes); // Get elements
    let tempPage = document.createElement("div"); // Container for one page

    for (let element of elements) {
        // Skip empty text nodes or whitespace
        if (element.nodeType === Node.TEXT_NODE && element.textContent.trim() === "") {
            continue;
        }

        let clonedElement = element.cloneNode(true);
        tempPage.appendChild(clonedElement); // Add element
        tempContainer.innerHTML = tempPage.innerHTML; // Insert into temp container

        // 🔥 If content overflows, handle it
        if (tempContainer.scrollHeight > availableHeight) {
            tempPage.removeChild(tempPage.lastChild); // Remove overflowing element

            // 🔥 Handle long paragraphs by splitting them into smaller chunks
            if (clonedElement.nodeName === "P") {
                let words = clonedElement.textContent.split(" ");
                let newParagraph = document.createElement("p");
                let tempText = "";
            
                for (let word of words) {
                    tempText += word + " ";
                    newParagraph.textContent = tempText.trim();
                    tempContainer.innerHTML = tempPage.innerHTML + newParagraph.outerHTML;
            
                    if (tempContainer.scrollHeight > availableHeight) {
                        let sentenceEndIndex = tempText.lastIndexOf(". "); // Try to split at full stop
                        if (sentenceEndIndex === -1) {
                            sentenceEndIndex = tempText.lastIndexOf(", "); // Otherwise, try a comma
                        }
                        if (sentenceEndIndex === -1) {
                            sentenceEndIndex = tempText.lastIndexOf(" "); // Otherwise, use the last space
                        }
                    
                        let firstPart = tempText.slice(0, sentenceEndIndex + 1).trim();
                        let remainingPart = tempText.slice(sentenceEndIndex + 1).trim();
                    
                        if (firstPart) {
                            newParagraph.textContent = firstPart;
                            tempPage.appendChild(newParagraph.cloneNode(true));
                        }
                        
                        pages.push(tempPage.innerHTML);
                        tempPage = document.createElement("div");
                    
                        if (remainingPart) {
                            let nextParagraph = document.createElement("p");
                            nextParagraph.textContent = remainingPart;
                            tempPage = document.createElement("div"); // Create a new page
                            tempPage.appendChild(nextParagraph);
                        }
                        
                    
                        break;
                    }
                    
                }
            } else {
                // For non-paragraph elements, move them to the next page
                pages.push(tempPage.innerHTML);
                tempPage = document.createElement("div");
                tempPage.appendChild(clonedElement.cloneNode(true));
            }
            
        }
    }

    // 🔥 Add the last page if it has content
    if (tempPage.innerHTML.trim() !== "") {
        pages.push(tempPage.innerHTML); // Store last page
    }

    totalPagesSpan.textContent = `/ ${pages.length}`; // Update total pages
    document.body.removeChild(tempContainer); // Cleanup
    if (tempContainer.scrollHeight > availableHeight) {
        while (tempContainer.scrollHeight > availableHeight && tempPage.lastChild) {
            tempPage.removeChild(tempPage.lastChild);
        }
        pages.push(tempPage.innerHTML);
    }    
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
let resizeTimeout;
window.addEventListener("resize", () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        let prevPage = currentPage; // Save current page
        paginateContent(); // Recalculate pages
        displayPage(prevPage); // Restore previous page
    }, 300); // Delay to prevent rapid resizing
});
