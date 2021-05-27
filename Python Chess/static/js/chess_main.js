let white = document.querySelector(".white");
let black = document.querySelector(".black");
let color = document.querySelector("#send_color");
white.style.backgroundColor = "rgb(255,215,0)";

function show_vsmodal(){
    $('#modal1').modal("show")
}

function hide_vsmodal(){
    $('#modal1').modal("hide")
}

function show_spmodal(){
    $('#modal2').modal("show")
}

function hide_spmodal(){
    $('#modal2').modal("hide")
}

function choose_white() {
    color.value = "white"
    white.style.backgroundColor = "rgb(255,215,0)";
    black.style.backgroundColor = "white";
}

function choose_black() {
    color.value = "black"
    black.style.backgroundColor = "rgb(255,215,0)";
    white.style.backgroundColor = "white";  
}