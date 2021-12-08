let starting_fen = document.getElementById("starting_fen").innerHTML;
let reset_text = document.getElementById("reset_text")
let start_button = document.getElementById("startBtn")
let model1 = document.getElementById("model1").innerHTML;
let model2 = document.getElementById("model2").innerHTML;
let player1 = document.getElementById("player1");
let player2 = document.getElementById("player2");
let history = document.getElementById("history");
let scrollbox = document.getElementById("scrollbox");
let minutes1 = document.getElementById("minutes1");
let minutes2 = document.getElementById("minutes2");
let seconds1 = document.getElementById("seconds1");
let seconds2 = document.getElementById("seconds2");
let t1box = document.getElementById("t1box");
let t2box = document.getElementById("t2box");
let timer1;
let timer2;
let time_increment = 10;
let snd = document.getElementById("myAudio"); 

let board = ChessBoard('board', {
   position: starting_fen,
   draggable: true,
   showNotation: true,
   moveSpeed: 'fast',
   snapbackSpeed: 500,
   snapSpeed: 100
});
let isgameover = false;
let reset = false;

set_names();
let moves = 0;
let turn = 1;

function reset_board(){
    
    start_button.disabled = true
    reset_text.style.display = "block";
    reset = true;
    isgameover = false;
    board.position('start')
    clearInterval(timer1);
    t1box.style.backgroundColor = "#C8C8C8";
    t1box.style.boxShadow = "none";
    clearInterval(timer2);
    t2box.style.backgroundColor = "#C8C8C8";
    t2box.style.boxShadow = "none";
    
    fetch('/reset', {
     
     headers: {'Content-Type': 'application/json'},
     method: 'POST',
     body: JSON.stringify({"reset": "true"})
     }).then(function (response) { 
         return response.text();
     }).then(function (text) {
         console.log('POST response: ');
         console.log(text);
     });
     
     history.innerHTML = "Move History:";
     moves = 0;
     minutes1.innerHTML = "10";
     minutes2.innerHTML = "10";
     seconds1.innerHTML = "00";
     seconds2.innerHTML = "00";
     setTimeout(() => {  start_button.disabled = false; reset_text.style.display = "none"; }, 5000);
     clearInterval(timer1);
     clearInterval(timer2);
     history.innerHTML = "Move History:"; 
    
}

async function fetch_move(){  
    reset = false; 
    isgameover = false;
    start_button.disabled = true
    
    if(reset==true){
            board.position('start')
            console.log("reset1")
            reset_board();
            return;
    }
    
    if (turn === 1){
        timer2 = setInterval(() => { start_timer(seconds2, minutes2, 1); }, 1000); 
        t2box.style.backgroundColor = "white";
        t2box.style.boxShadow = "2px 3px #696969";
    }
    else{
        timer1 = setInterval(() => { start_timer(seconds1, minutes1, -1); }, 1000); 
        t1box.style.backgroundColor = "white";
        t1box.style.boxShadow = "2px 3px #696969";
    }
     
    if (isgameover === false && reset === false){
        
       await fetch('/selfmove')
           .then(async function (response) {         
               return await response.json();
           }).then(function (text) {
               if(text.isgameover == false && reset==false){
                   console.log('GET response:');
                   console.log(text.move); 
                   console.log(text.player); 
                   console.log(text.fen);
                   console.log(text.isgameover)
                   board.position(text.fen)
                   snd.play();
                   
               }
           
           if (text.player === "White"){
                moves = moves + 1
                history.innerHTML = history.innerHTML.concat("<br>" + moves + ". " + text.move)
                scrollbox.scrollTop = scrollbox.scrollHeight; 
                clearInterval(timer2);
                add_increment(seconds2, minutes2, time_increment)
                t2box.style.backgroundColor = "#C8C8C8";
                t2box.style.boxShadow = "none"; 
            }
            else{
                history.innerHTML = history.innerHTML.concat("  " + text.move)
                clearInterval(timer1);
                add_increment(seconds1, minutes1, time_increment)
                t1box.style.backgroundColor = "#C8C8C8";
                t1box.style.boxShadow = "none";
            }
           
           turn = turn*(-1);
           isgameover = text.isgameover;
           if (isgameover === false && reset === false){
               fetch_move();
           }
           //else{
           //    reset_board();
           //}
    });
    }  
    
    if (isgameover === true){
        await fetch('/selfmove')
         .then(async function (response) {         
             return await response.json();
         }).then(function (text) {
             console.log('GET response:');
             console.log(text.result);  
             console.log(text.msg);
             
             history.innerHTML = history.innerHTML.concat("<br> <b>" + text.msg + "</b>")
             scrollbox.scrollTop = scrollbox.scrollHeight; 
             clearInterval(timer1);
             clearInterval(timer2);
    });
    }
    
}

function set_names(){
    
    let player1_title = "PCE Self-Trained Model"
    let player2_title = "PCE Self-Trained Model"
    
    if (model1 == "2"){
        player1_title = "PCE Data-Trained Model";
    }
    else if (model1 == "3"){
        player1_title = "PCE Combined Model";
    }
    else if (model1 == "4"){
        player1_title = "Stockfish Chess Engine";
    }
    if (model2 == "2"){
        player2_title = "PCE Data-Trained Model";
    }
    else if (model2 == "3"){
        player2_title = "PCE Combined Model";
    }
    else if (model2 == "4"){
        player2_title = "Stockfish Chess Engine";
    }
    
    player2.innerHTML = player1_title;
    player1.innerHTML = player2_title;
    
}

function start_timer( secs, mins, color){
    s = secs.innerHTML - 1;
    m = mins.innerHTML;
    
    if (s>9){
        secs.innerHTML = secs.innerHTML - 1;
    }
    else if(s>-1 && s<10){
        secs.innerHTML = "0" + (secs.innerHTML - 1);
    }
    else{
        if(m>1 && m<10){
            mins.innerHTML = "0" + (mins.innerHTML - 1);
            secs.innerHTML = 59;
        }
        else if(m>1){
            mins.innerHTML = mins.innerHTML - 1;
            secs.innerHTML = 59;
        }
        else if( m == 1){
            mins.innerHTML = "00";
            secs.innerHTML = 59;
        }
        else{
            mins.innerHTML = "00";
            secs.innerHTML = "00";
            clearInterval(timer1);
            clearInterval(timer2);
            t2box.style.backgroundColor = "#C8C8C8";
            t2box.style.boxShadow = "none";
            t1box.style.backgroundColor = "#C8C8C8";
            t1box.style.boxShadow = "none";
            
            if(color === 1){
                history.innerHTML = history.innerHTML.concat("<br> <b>White out of time. Black Wins!</b>")
                scrollbox.scrollTop = scrollbox.scrollHeight;
            }
            else if(color === -1){
                history.innerHTML = history.innerHTML.concat("<br> <b>Black out of time. White Wins!</b>")
                scrollbox.scrollTop = scrollbox.scrollHeight;
            }
            
            isgameover = true;
            clearInterval(timer1);
            clearInterval(timer2);
        }
    }
    
}

function add_increment(seconds, minutes, increment){

    s = parseInt(seconds.innerHTML);
    if ((s + increment) < 60){
        seconds.innerHTML = parseInt(s) + increment;
    }
    else{
        diff = parseInt(s + increment - 60);
        if (minutes.innerHTML < 9){
            minutes.innerHTML = "0" + parseInt(parseInt(minutes.innerHTML) + 1);
        } 
        else{
            minutes.innerHTML = parseInt(parseInt(minutes.innerHTML) + 1);
        }
        seconds.innerHTML = "0" + parseInt(diff);
    }
}

