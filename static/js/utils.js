function addNotification(message, color) {
	const container = document.getElementById('notifications-container')
    container.classList.add('p-4')
	// Create notification element
	const notification = document.createElement('div')
	notification.className = `min-w-32 bg-${color}-200 rounded-sm shadow-lg`

	// Create notification message
	const messageDiv = document.createElement('div')
	messageDiv.className = `py-2 px-4 rounded-t-sm bg-${color}-200`
	messageDiv.textContent = message

	// Create progress bar
	const progressBar = document.createElement('div')
	progressBar.className = `h-1.5 rounded-b-sm bg-${color}-400 transition-all duration-[3000ms]`
	progressBar.style.width = '100%'

	// Append message and progress bar to notification
	notification.appendChild(messageDiv)
	notification.appendChild(progressBar)

	// Append notification to container
	container.appendChild(notification)

	// Start progress bar animation
	setTimeout(function () {
		progressBar.style.width = '0%'
	}, 10)

	setTimeout(function () {
		notification.remove()
        container.classList.remove('p-4')
	}, 3000)
}


function submitComment(form, event) {
    event.preventDefault(); // Prevent default form submission immediately

    const input = form.querySelector("#comment-input");
    const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    const url = form.getAttribute("data-url");
    const bookId = form.getAttribute("data-book-id");
    const parentId = form.getAttribute("data-parent-id");

    let comment = input.value.trim();
    if (comment === "") return; // Prevent empty submissions

    let formData = new FormData();
    formData.append("comment", comment);
    formData.append("csrfmiddlewaretoken", csrftoken); // Django CSRF token
    formData.append("book_id", bookId);
    formData.append("parent_id", parentId);

    fetch(url, {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(result => {
        document.getElementById("comment-count").textContent = result.comment_count;

        let div = document.createElement("div");
        div.classList.add("flex", "space-x-2", "flex-wrap");
        div.setAttribute("data-id", result.comment_id);
        div.setAttribute("data-book-id", result.book_id)
        div.innerHTML = `
            <img alt="" class="h-10 w-10 rounded-full" src="${result.profile_img}" />
            <div>
                <div class="text-sm font-medium">
                    @${result.username}
                    <span class="text-sm font-thin">Just Now</span>
                </div>
                <div class="text-base">${comment}</div>
                <div class="flex space-x-3 text-sm items-center">
                    <div class="font-extralight">
                        <button><i class="fa-regular fa-thumbs-up"></i></button>
                    </div>
                    <div class="font-medium">
                        <button><i class="fa-regular fa-thumbs-down"></i></button>
                    </div>
                    <button class="p-2 font-bold rounded-full hover:bg-gray-200" onclick="replyForm(this)">Reply</button>
                    <a onclick="delete_comment(this)" class="text-red-500 cursor-pointer">Delete</a>
                </div>
            </div>
        `;
        if(result.reply){
            div.classList.add('ml-10')
            document.querySelector(`[data-id="${result.parent_id}"]`).insertAdjacentElement('afterend', div)
        }else{
            let comments = document.getElementById("comments-container");
        comments.insertBefore(div, comments.children[0]);
        }

        
        addNotification("Comment added", "green");
        console.log("Comment submitted:", result);
        input.value = ""; // Clear input on success
    })
    .catch(error => console.error("Request failed:", error));
}
