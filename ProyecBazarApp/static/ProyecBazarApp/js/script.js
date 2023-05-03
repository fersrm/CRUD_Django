let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".bx-menu");
let hambur= document.getElementById("MenuHambur");

let contenido = document.getElementById("body");

//console.log(sidebarBtn);
sidebarBtn.addEventListener("click", ()=>{
  sidebar.classList.toggle("close");
  hambur.classList.toggle("activo");
  contenido.classList.toggle("none");
});