let modalAgregar = document.getElementById("agregar");
let modalEditar = document.getElementById("edicion");
// Cuando el usuario hace clic en el botón de cerrar, ocultar la ventana modal
function cerrar_modal_add() {
  modalAgregar.style.display = "none";
}
function cerrar_modal_editar(){
  modalEditar.style.display = "none";
}
// Cuando el usuario hace clic fuera de la ventana modal, ocultarla
window.onclick = function(event) {
  if (event.target == modalAgregar) {
    modalAgregar.style.display = "none";
  }
  else if (event.target == modalEditar) {
    modalEditar.style.display = "none";
  }
}
//----------------------------------------------------------

function abrir_modal_edicion(url){
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("edicion").innerHTML = this.responseText;
      document.getElementById("edicion").style.display = "flex";
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
};

function abrir_modal_creacion(url){
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("agregar").innerHTML = this.responseText;
      document.getElementById("agregar").style.display = "flex";
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
};
