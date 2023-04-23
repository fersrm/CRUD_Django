let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".bx-menu");
let hambur= document.getElementById("MenuHambur");
//console.log(sidebarBtn);
sidebarBtn.addEventListener("click", ()=>{
  sidebar.classList.toggle("close");
  hambur.classList.toggle("activo");
});



//----------------------MODAL--------------------------------------
let modal = document.getElementById("agregar-producto");
let btn = document.getElementById("abrir-modal");
let span = document.getElementById("cerrar-modal");
// Cuando el usuario hace clic en el botón, mostrar la ventana modal
btn.onclick = function() {
  modal.style.display = "flex";
}
// Cuando el usuario hace clic en el botón de cerrar, ocultar la ventana modal
span.onclick = function() {
  modal.style.display = "none";
}
// Cuando el usuario hace clic fuera de la ventana modal, ocultarla
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}