// Modal and tab logic
const modal = document.getElementById("modal");
const openModalBtn = document.getElementById("openModalBtn");
const closeModalBtn = document.getElementById("closeModalBtn");
const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");
const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

// Open modal
openModalBtn.addEventListener("click", () => {
    modal.classList.remove("hidden");
    modal.classList.add("flex");

});

// Close modal
closeModalBtn.addEventListener("click", () => {
    modal.classList.add("hidden");
    modal.classList.remove("flex");
});

// Switch to login form
loginTab.addEventListener("click", () => {
    loginForm.classList.remove("hidden");
    registerForm.classList.add("hidden");
    loginTab.classList.add("text-blue-500", "border-b-2", "border-blue-500");
    registerTab.classList.remove("text-blue-500", "border-b-2", "border-blue-500");
});

// Switch to register form
registerTab.addEventListener("click", () => {
    registerForm.classList.remove("hidden");
    loginForm.classList.add("hidden");
    registerTab.classList.add("text-blue-500", "border-b-2", "border-blue-500");
    loginTab.classList.remove("text-blue-500", "border-b-2", "border-blue-500");
});
