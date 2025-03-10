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
// function paginateContent() {
//     pages = [];
//     tempContainer.innerHTML = ""; // Clear previous content
//     tempContainer.style.width = pageContainer.clientWidth + "px"; // Match width
//     tempContainer.style.position = "absolute"; // Prevent layout shifting
//     tempContainer.style.visibility = "hidden"; // Hide from view
//     document.body.appendChild(tempContainer); // Append for measurement

//     // 🔥 Get padding values dynamically
//     const computedStyle = window.getComputedStyle(pageContainer);
//     const paddingTop = parseFloat(computedStyle.paddingTop);
//     const paddingBottom = parseFloat(computedStyle.paddingBottom);
//     const availableHeight = pageContainer.clientHeight - (paddingTop + paddingBottom); // Adjust height

//     let content = document.createElement("div");
//     content.innerHTML = bookContent; // Convert string to actual HTML elements
//     let elements = Array.from(content.childNodes); // Get elements
//     let tempPage = document.createElement("div"); // Container for one page

//     for (let element of elements) {
//         let clonedElement = element.cloneNode(true);
//         tempPage.appendChild(clonedElement); // Add element
//         tempContainer.innerHTML = tempPage.innerHTML; // Insert into temp container

//         // 🔥 If content overflows, we need to break it
//         if (tempContainer.scrollHeight > availableHeight) {
//             tempPage.removeChild(tempPage.lastChild); // Remove overflowing element

//             // 🔥 Special handling for long paragraphs (split by line)
//             if (clonedElement.nodeName === "P") {
//                 let words = clonedElement.innerHTML.split(" ");
//                 let newParagraph = document.createElement("p");
//                 let tempText = "";

//                 for (let word of words) {
//                     tempText += word + " ";
//                     newParagraph.innerHTML = tempText;
//                     tempContainer.innerHTML = tempPage.innerHTML + newParagraph.outerHTML;

//                     if (tempContainer.scrollHeight > availableHeight) {
//                         tempText = tempText.trim().split(" ").slice(0, -1).join(" ");
//                         newParagraph.innerHTML = tempText;
//                         tempPage.appendChild(newParagraph.cloneNode(true));
//                         pages.push(tempPage.innerHTML); // Save full page
//                         tempPage = document.createElement("div"); // Start new page
//                         newParagraph.innerHTML = word + " ";
//                         tempPage.appendChild(newParagraph.cloneNode(true));
//                         break;
//                     }
//                 }
//             } else {
//                 pages.push(tempPage.innerHTML); // Store full page
//                 tempPage = document.createElement("div"); // Start new page
//                 tempPage.appendChild(clonedElement.cloneNode(true)); // Move overflowed element
//             }
//         }
//     }

//     pages.push(tempPage.innerHTML); // Store last page
//     totalPagesSpan.textContent = `/ ${pages.length}`; // Update total pages
//     document.body.removeChild(tempContainer); // Cleanup
//     displayPage(0);
// }

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
    const availableHeight = pageContainer.clientHeight - (paddingTop + paddingBottom); // Adjust height

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
                        // Remove the last word and save the current page
                        tempText = tempText.trim().split(" ").slice(0, -1).join(" ");
                        newParagraph.textContent = tempText;
                        tempPage.appendChild(newParagraph.cloneNode(true));
                        pages.push(tempPage.innerHTML); // Save full page
                        tempPage = document.createElement("div"); // Start new page
                        newParagraph.textContent = word + " ";
                        tempPage.appendChild(newParagraph.cloneNode(true));
                        break;
                    }
                }
            } else {
                // For non-paragraph elements, just move them to the next page
                pages.push(tempPage.innerHTML); // Store full page
                tempPage = document.createElement("div"); // Start new page
                tempPage.appendChild(clonedElement.cloneNode(true)); // Move overflowed element
            }
        }
    }

    // 🔥 Add the last page if it has content
    if (tempPage.innerHTML.trim() !== "") {
        pages.push(tempPage.innerHTML); // Store last page
    }

    totalPagesSpan.textContent = `/ ${pages.length}`; // Update total pages
    document.body.removeChild(tempContainer); // Cleanup
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
