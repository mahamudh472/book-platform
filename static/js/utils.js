function addNotification(message, color) {
    const container = document.getElementById('notifications-container')
  
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
    }, 3000)
  }