

// sideBar Toggle handling
document.getElementById('menuToggle').addEventListener('click', function (event) {
    event.stopPropagation()
    const sideBar = document.getElementById('sidebar')
    const menuItems = document.getElementsByClassName('menu-item')
    const cardGrid = document.getElementById('content')

    if (screen.width < 768) {
        fullMenuHide = true
        halfMenu = false
        if (screen.width < 640) {
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

// document.addEventListener('click', (event) => {
//     const sideBar = document.getElementById('sidebar')
//     if (fullMenuHide == true) {
//         if (!sideBar.classList.contains('left-[-100%]')) {
//             sideBar.classList.add('left-[-100%]');
//         }
//     }

// });



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
    followBtn.addEventListener('click', function () {
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


const likeDislikeBtns = document.querySelectorAll('#like-dislike-btn');

if (likeDislikeBtns.length > 0) {  // Ensure at least one button exists
    likeDislikeBtns.forEach((element) => {
        element.addEventListener('click', function () {
            let bookId = element.getAttribute("data-book-id");  // Store book ID in `data-user-id`
            let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            let likeUrl = element.getAttribute("data-url");
            let op = element.getAttribute("data-op");
            let likeBtn = document.querySelector("[data-op=like]")
            let dislikeBtn = document.querySelector("[data-op=dislike]")

            fetch(likeUrl, {  // Ensure correct URL
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrftoken
                },
                body: `book_id=${bookId}&op=${op}`
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                    if (data.status === "success") {
                        if (op==="like"){
                            likeBtn.querySelector('i').classList.toggle('fa-regular')
                            likeBtn.querySelector('i').classList.toggle('fa')
                            likeBtn.querySelector('div').textContent = data.likes
                            dislikeBtn.querySelector('div').textContent = data.dislikes
                            if (dislikeBtn.querySelector('i').classList.contains('fa')){
                                dislikeBtn.querySelector('i').classList.remove('fa')
                                dislikeBtn.querySelector('i').classList.add('fa-regular')
                            }
                        }else if(op==="dislike"){
                            dislikeBtn.querySelector('i').classList.toggle('fa-regular')
                            dislikeBtn.querySelector('i').classList.toggle('fa')
                            likeBtn.querySelector('div').textContent = data.likes
                            dislikeBtn.querySelector('div').textContent = data.dislikes
                            if (likeBtn.querySelector('i').classList.contains('fa')){
                                likeBtn.querySelector('i').classList.remove('fa')
                                likeBtn.querySelector('i').classList.add('fa-regular')
                            }
                        }
                        
                    }
                    // document.getElementById('likes_count').textContent = `${data.likes_count}`;
                })
                .catch(error => console.log("Error:", error));
        });
    })

}


document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("comment-form");
    const input = document.getElementById("comment-input");
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let url = form.getAttribute('data-url')
    let bookId = form.getAttribute("data-book-id")

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission

        let comment = input.value.trim();
        if (comment === "") return; // Prevent empty submissions

        let formData = new FormData();
        formData.append("comment", comment);
        formData.append("csrfmiddlewaretoken", `${csrftoken}`); // Django CSRF token
        formData.append("book_id", bookId)

        try {
            let response = await fetch(url, {
                method: "POST",
                body: formData,
            });

            if (response.ok) {
                let result = await response.json();
                console.log("Comment submitted:", result);
                input.value = ""; // Clear input on success
            } else {
                console.error("Error submitting comment:", response.statusText);
            }
        } catch (error) {
            console.error("Request failed:", error);
        }
    });
});

