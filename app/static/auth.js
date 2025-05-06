
function closeBox(){
  window.location.href ="/";
}


function auth_msg_handler(){
    const message = document.getElementById("message");
    const message_status = document.getElementById("category");
    const notification = document.getElementById('notification');
    console.log("1 From auth js", message, message_status)
    notification.innerText = message.innerText;
    if (message_status.innerText === "error"){
          notification.style.backgroundColor = "rgba(202, 10, 10, 0.77)";
      }else{
          notification.style.backgroundColor = "rgba(57, 235, 13, 0.77)";
      }
    
    notification.classList.add('show');
    setTimeout(() => {
        notification.classList.remove('show');
        notification.style.top = "-90px";
      }, 3000);
    console.log("2 From auth js", notification, notification.innerText)
}


window.addEventListener('load', ()=>{
  auth_msg_handler()
  
});

