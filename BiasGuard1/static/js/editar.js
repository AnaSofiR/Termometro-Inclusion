let circuloGenero = document.querySelector(".circuloGenero"),
    circuloEdad = document.querySelector(".circuloEdad"),
    valorGenero = document.querySelector(".valorGenero"),
    valorEdad = document.querySelector(".valorEdad"),
    numeroGenero = document.querySelector(".numeroValorGenero"),
    numeroEdad = document.querySelector(".numeroValorEdad");

let valorInicialGenero = -1,
    valorFinalGenero = numeroGenero.value;
    
let valorInicialEdad = -1,
    valorFinalEdad = numeroEdad.value;

let speed = 100;


let progresoGenero = setInterval(() => {
    valorInicialGenero++;

    valorGenero.textContent = `${valorInicialGenero}%`
    circuloGenero.style.background = `conic-gradient(#ff0000 ${valorInicialGenero * 3.6}deg, #d3d3d3 0deg)`
    

    if(valorInicialGenero == valorFinalGenero || valorInicialGenero >= 100){
        console.log(valorFinalEdad)
        clearInterval(progresoGenero);
    }
}, speed)


let progresoEdad = setInterval(() => {
    valorInicialEdad++;

    valorEdad.textContent = `${valorInicialEdad}%`
    circuloEdad.style.background = `conic-gradient(#ecab0f ${valorInicialEdad * 3.6}deg, #d3d3d3 0deg)`

    if(valorInicialEdad == valorFinalEdad){
        clearInterval(progresoEdad);
    }
}, speed)

let divTexto = document.querySelector(".sugerencia");
let divReemplazar = document.querySelector(".reemplazar")
function sugerencia() {
    // Obtener el elemento div por su id
    var divTexto = document.querySelector(".sugerencia");
    var divBoton = document.querySelector(".generarSugerencia")
    var divReemplazar = document.querySelector(".reemplazar")

    // Cambiar el estilo para mostrar el div
    divTexto.style.visibility = "visible";
    divReemplazar.style.visibility = "visible";
    divBoton.style.visibility = "hidden";
    divBoton.style.margin = "0px";
    

}

function recomendacionGenero() {
    // Obtener el elemento div por su id
    var divTexto = document.querySelector(".recomendacionGenero");

    // Cambiar el estilo para mostrar el div
    divTexto.style.visibility = "visible";
}

function recomendacionEdad() {
    // Obtener el elemento div por su id
    var divTexto = document.querySelector(".recomendacionEdad");

    // Cambiar el estilo para mostrar el div
    divTexto.style.visibility = "visible";
}


function reemplazar(){
    var sugerencia = document.querySelector(".descripcionSugerencia");
    var descripcion = document.querySelector(".description");
    var divTexto = document.querySelector(".sugerencia");
    var divReemplazar = document.querySelector(".reemplazar")

    descripcion.innerHTML = sugerencia.value;
    divTexto.style.visibility = "hidden";
    divReemplazar.style.visibility = "hidden";
}

