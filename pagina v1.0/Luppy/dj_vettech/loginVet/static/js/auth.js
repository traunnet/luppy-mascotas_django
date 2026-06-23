document.querySelectorAll(".link-switch").forEach(link => {link.addEventListener("click", function(e){
e.preventDefault();
document.querySelector(".auth-card").style.opacity = "0";
document.querySelector(".auth-card").style.transform = "translateY(-30px)";
setTimeout(()=>{window.location = this.href;},400);
});
});
