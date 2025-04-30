
function closeBox(){
  window.location.href ="/api/home";
}


function auth_msg_handler(){
    const message = document.getElementById("message");
    const message_status = document.getElementById("category");
    const notification = document.getElementById('notification');
    
    if (window.location.href.includes("/auth")){
    notification.innerText = message.innerText;
    if (message_status.innerText === "error"){
          notification.style.backgroundColor = "rgba(202, 10, 10, 0.77)";
      }
    
    if (message_status.innerText === "success"){
          notification.style.backgroundColor = "rgba(57, 235, 13, 0.77)";
      }
    
      notification.classList.add('show');
      setTimeout(() => {
          notification.classList.remove('show');
          notification.style.top = "-90px";
        }, 3000);
  }
}


window.addEventListener('DOMContentLoaded', ()=>{
  auth_msg_handler()
  
});

