const readNowButton = document.getElementById('read-now-btn')
const coverContainer = document.getElementById('cover-container')
const readerContainer = document.getElementById('reader-container')
const pageContainer = document.getElementById('page-container')

readNowButton.addEventListener('click', function(){
    coverContainer.classList.add('hidden');
    readerContainer.classList.remove('hidden')
})