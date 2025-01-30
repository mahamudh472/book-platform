

// sideBar Toggle handling
document.getElementById('menuToggle').addEventListener('click', function (event) {
    event.stopPropagation()
    const sideBar = document.getElementById('sidebar')
    const menuItems = document.getElementsByClassName('menu-item')
    const cardGrid = document.getElementById('content')

    if (screen.width<768){
        fullMenuHide = true
        halfMenu = false
        if (screen.width<640){
            sideBar.classList.toggle('w-full')
        }
    }

    if (halfMenu == true) {
        sideBar.classList.toggle('md:w-64')
        sideBar.classList.toggle('md:w-18')
        sideBar.classList.toggle('p-4')
        sideBar.classList.toggle('py-3')
        cardGrid.classList.toggle('md:ml-64')
        cardGrid.classList.toggle('md:ml-32')

        Array.from(menuItems).forEach(element => {
            element.classList.toggle('flex-col')
            element.classList.toggle('text-xs')
            element.classList.toggle('space-x-3')
            element.querySelector('span').classList.toggle('whitespace-normal')
        });
    }

    if (fullMenuHide == true) {
        sideBar.classList.toggle('-translate-x-full')
    }

})

document.addEventListener('click', (event) => {
    const sideBar = document.getElementById('sidebar')
    if (fullMenuHide == true) {
        if (!sideBar.classList.contains('left-[-100%]')) {
            sideBar.classList.add('left-[-100%]');
        }
    }

});



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


const followBtn = document.getElementById('follow-btn');

if (followBtn) {
    followBtn.addEventListener('click', function() {
        let userId = followBtn.getAttribute("data-user-id");  // Store user ID in `data-user-id`
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        let followUrl = followBtn.getAttribute("data-url");

        fetch(followUrl, {  // Ensure correct URL
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrftoken
            },
            body: `user_id=${userId}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === "followed") {
                followBtn.textContent = "Unfollow";
                addNotification(`Following ${data.target_user}`, 'green')
            } else if (data.status === "unfollowed") {
                followBtn.textContent = "Follow";
                addNotification(`Unfollowed ${data.target_user}`, 'red')
            }
            document.getElementById('followers_count').textContent = `${data.followers_count}`;
        })
        .catch(error => console.log("Error:", error));
    });
}
