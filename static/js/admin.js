
// Left side menus 
document.getElementById("menuToggle").addEventListener('click', () => {
    // initializing the components
    const sidebar = document.getElementById('sidebar')
    const sidebarImg = document.getElementById('sidebar_profile_img')
    const mainContainer = document.querySelector('main')
    const sidebarItems = document.querySelector('#sidebarItems')
    const backText = document.getElementById('back_text')

    // sidebar and content box sizing
    sidebar.classList.toggle('w-64')
    sidebar.classList.toggle('w-12')
    sidebar.classList.toggle('p-4')
    sidebar.classList.toggle('p-0')


    mainContainer.classList.toggle('ml-64')
    mainContainer.classList.toggle('ml-16')

    // sidebar profile image sizing
    sidebarImg.classList.toggle('h-24')
    sidebarImg.classList.toggle('w-24')
    sidebarImg.classList.toggle('h-10')
    sidebarImg.classList.toggle('w-10')
    sidebarImg.classList.toggle('m-auto')

    if (backText) {
        backText.classList.toggle('hidden')
    }

    // sidebar image bottom text toggle 
    sidebarImg.parentElement.querySelectorAll('div').forEach(element => {
        element.classList.toggle('hidden')
    })
    // sidebar menu text toggle 
    sidebarItems.querySelectorAll('li > span').forEach(element => {
        element.classList.toggle('hidden')
    })
    // sidebar menu icons resize 
    sidebarItems.querySelectorAll('li > i').forEach(element => {
        element.classList.toggle('w-6')
    })
    sidebarItems.querySelectorAll('li').forEach(element => {
        element.classList.toggle('justify-center')
    })


})



// --------------------------------------------------
// ----------------- Dropdown menu-------------------
// --------------------------------------------------

// Handle dropdown toggle
document.querySelectorAll('.dropdownButton').forEach(button => {
    button.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent the event from propagating to the document
        const menu = this.nextElementSibling; // Get the corresponding dropdown menu
        menu.classList.toggle('hidden');
        // Close other open dropdowns
        document.querySelectorAll('.dropdownMenu').forEach(otherMenu => {
            if (otherMenu !== menu) {
                otherMenu.classList.add('hidden');
            }
        });
    });
});

// Close dropdowns when clicking outside
document.addEventListener('click', (event) => {
    document.querySelectorAll('.dropdownMenu').forEach(menu => {
        if (!menu.classList.contains('hidden')) {
            menu.classList.add('hidden');
        }
    });
});



// active menu 
document.addEventListener("DOMContentLoaded", () => {
    const menuItems = document.querySelectorAll(".menu-item");

    // Get the current page from the URL
    const currentPage = window.location.pathname.split("/").pop();

    menuItems.forEach(item => {
        const page = item.getAttribute("data-page");

        if (page === currentPage) {
            item.classList.add("bg-gray-100", "font-bold");
            item.querySelector("span").classList.add("text-gray-700");
        } else {
            item.classList.remove("bg-gray-100", "font-bold");
            item.querySelector("span").classList.remove("text-gray-700");
        }
    });
});





//  copy text to clipboard
function copy_to_clipboard(btn) {
    const linkText = document.getElementById('book_link').innerText
    navigator.clipboard.writeText(linkText)
    btn.classList.toggle('fa-regular')
    btn.classList.toggle('fa-copy')
    btn.classList.toggle('fa')
    btn.classList.toggle('fa-check')
}
