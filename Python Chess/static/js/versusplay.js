let starting_fen = document.getElementById("starting_fen").innerHTML;
let first_legal_moves = document.getElementById("first_moves").innerHTML
                  .replace("[","").replace("]","").replace(/'/gi, "").split(", ");
let orientation = document.getElementById("player_color").innerHTML;
let legal_moves = get_first_moves();
let reset_button = document.getElementById("resetBtn");
let sur_button = document.getElementById("surrenderBtn");
let opponent = document.getElementById("opponent").innerHTML;
let player1 = document.getElementById("player1");
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

let moves = 0;            
let isgameover = false;
let turn = true;
let reset = false;

let board = ChessBoard('board', {
   position: starting_fen,
   draggable: true,
   showNotation: true,
   moveSpeed: 'fast',
   snapbackSpeed: 500,
   snapSpeed: 100,
   onDragStart: onDragStart,
   onDrop: onDrop,
   orientation: orientation,
   onMouseoverSquare: onMouseoverSquare,
   onMouseoutSquare: onMouseoutSquare
});

set_names();
white_move_first();


function reset_board(){
   reset = true;
   reset_button.disabled = true;
   reset_text.style.display = "block";
   isgameover = false;
   turn = true;
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
    
    setTimeout(() => { start_new_game(); }, 5000); 
    moves = 0;
}

function start_new_game(){
    
    board.position(starting_fen)
    reset_text.style.display = "none";
    reset = false;
    reset_button.disabled = false;
    if(orientation === "white"){
        legal_moves = first_legal_moves;
    }
    else{
        legal_moves = [];
        white_move_first();
    }
    
    minutes1.innerHTML = "10";
    minutes2.innerHTML = "10";
    seconds1.innerHTML = "00";
    seconds2.innerHTML = "00";
    
}

function surrender(){
    
    if (orientation === "white"){
        history.innerHTML = history.innerHTML.concat("<br> <b> White surrendered. Black Wins! </b>")
    }
    
    else if (orientation === "black"){
        history.innerHTML = history.innerHTML.concat("<br> <b> Black surrendered. White Wins! </b>")
    }
    
    scrollbox.scrollTop = scrollbox.scrollHeight;
    reset_board();
}


function onDragStart(source, piece, position, orientation){
    
    if ((orientation === "white" && turn === false) || (orientation === "black" && turn === true)){
        console.log('snapback2')
        return
    }
    if(isgameover === true){
        return false}
    if((orientation === "white" && piece.search(/^w/) === -1) ||
       (orientation === "black" && piece.search(/^b/) === -1)){
       console.log('snapback3')
        return false
    }
}

function onDrop(source, target, piece, newPos, oldPos, orientation){
    
    removeGreySquares();
    if(reset==true){
        board.position(starting_fen)
        return;
    }
    
    let move = source.concat(target);
    
    if(orientation === "white" && piece.search(/P/) === 1 && target.search(/8/) === 1){
        move = move + 'q';
    }
    
    if(orientation === "black" && piece.search(/P/) === 1 && target.search(/1/) === 1){
        move = move + 'q';
    }
    
    if(!legal_moves.includes(move) || isgameover || (orientation === "white" && turn === false) ||
      (orientation === "black" && turn === true)){
      console.log('snapback1')
        return 'snapback'
    }
    
    
    console.log("Move: ", move)
    
    fetch('/post_move', {
        headers: {'Content-Type': 'application/json'},
        method: 'POST',
        body: JSON.stringify({"move": move})
        }).then(function (response) { 
            return response.text();
        }).then(function (text) {
            console.log('POST response: ');
            console.log(text);
            if(orientation === "white"){
                turn = false;
            }
            else{
                turn = true;
            }
            
            
    })
    clearInterval(timer2);
    add_increment(seconds2, minutes2, time_increment)
    t2box.style.backgroundColor = "#C8C8C8";
    t2box.style.boxShadow = "none";
    
    GET_data();
    
}

async function GET_data(){
    
    reset_button.disabled = true;
    [isgameover, turn] = await GET_board();
    
    if(isgameover===false){
        [isgameover, turn] = await GET_engine_move();
    }
    
    if(isgameover===true){
        GET_result();
    }
    reset_button.disabled = false;
}

function onMouseoverSquare (square, piece) {
    
    if ((orientation === "white" && turn === false) || (orientation === "black" && turn === true)){
        return
    }
    
    let square_moves = [];
    for(i=0; i<legal_moves.length; i++){
        source = legal_moves[i].substring(0,2);
        if(source === square){
            square_moves.push(legal_moves[i])
        }
    }
    
    if (square_moves.length === 0) return
    
    greySquare(square)
    for (let i = 0; i < square_moves.length; i++) {
      greySquare(square_moves[i].substring(2,4))
    }

}

let whiteSquareGrey = '#a9a9a9'
let blackSquareGrey = '#696969'

function greySquare (square) {
    var $square = $('#board .square-' + square)
    
    var background = whiteSquareGrey
    if ($square.hasClass('black-3c85d')) {
      background = blackSquareGrey
    }
    
    $square.css('background', background)
}

function removeGreySquares () {
  $('#board .square-55d63').css('background', '')
}

function onMouseoutSquare (square, piece) {
    removeGreySquares()
}

async function GET_board(){

    if(reset==true){
        board.position(starting_fen)
        return;
    }
        
    await fetch('/get_player_move')
        .then(async function (response) {         
            return await response.json();
        }).then(function (text) {
            if(text.isgameover == false && reset==false){
                board.position(text.fen)
                console.log('GET response:');
                console.log(text.move); 
                console.log(text.player); 
                console.log(text.fen);
                console.log(text.isgameover)
            }
        
        isgameover = text.isgameover;
        if(moves === 0){
            history.innerHTML = "Move History:"
        }
        if(orientation === "white"){
            moves = moves + 1
            turn = false;
            history.innerHTML = history.innerHTML.concat("<br>" + moves + ". " + text.move)
            scrollbox.scrollTop = scrollbox.scrollHeight; 
        }
        else{
            turn = true;
            history.innerHTML = history.innerHTML.concat("  " + text.move)
        }

    });
    
    return [isgameover, turn] ;
    
}

async function GET_engine_move(){
    
    if(reset==true){
        board.position(starting_fen)
        return;
    }
    
    if(orientation === "white"){
        timer1 = setInterval(() => { start_timer(seconds1, minutes1, "black"); }, 1000);
    }
    else{
        timer1 = setInterval(() => { start_timer(seconds1, minutes1, "white"); }, 1000);
    }
    t1box.style.backgroundColor = "white";
    t1box.style.boxShadow = "2px 3px #696969";
     
    
    await fetch('/get_engine_move')
         .then(async function (response) {         
             return response.json();
         }).then(await function (text) {
             if(text.isgameover == false && reset==false){
                 board.position(text.fen)
                 console.log('GET response:');
                 console.log(text.move); 
                 console.log(text.player); 
                 console.log(text.fen);
                 console.log(text.isgameover)
             }
             
             isgameover = text.isgameover;
             clearInterval(timer1);
             add_increment(seconds1, minutes1, time_increment)
             t1box.style.backgroundColor = "#C8C8C8";
             t1box.style.boxShadow = "none";
             legal_moves = text.legal_moves;
             if(moves === 0){
                 history.innerHTML = "Move History:"
             }
             if(orientation === "white"){
                 turn = true;
                 history.innerHTML = history.innerHTML.concat("  " + text.move)
             }
             else{
                 moves = moves + 1;
                 turn = false;
                 history.innerHTML = history.innerHTML.concat("<br>" + moves + ". " + text.move)
                 scrollbox.scrollTop = scrollbox.scrollHeight; 
                 
             }
             timer2 = setInterval(() => { start_timer(seconds2, minutes2, orientation); }, 1000); 
             t2box.style.backgroundColor = "white";
             t2box.style.boxShadow = "2px 3px #696969";
    });
    
    return [isgameover, turn] ;
    
}

async function GET_result(){
    
    await fetch('/get_result')
         .then(async function (response) {         
             return await response.json();
         }).then(function (text) {
             console.log('GET response:');
             console.log(text.result);  
             console.log(text.msg);
             
             history.innerHTML = history.innerHTML.concat("<br> <b>" + text.msg + "</b>")
             scrollbox.scrollTop = scrollbox.scrollHeight; 
        });
         
    return;
        
}

function get_first_moves(){
    
    let legal_moves = [];
    if(orientation === "white"){
        legal_moves = first_legal_moves;
    }

    return legal_moves;
}

async function white_move_first(){
    
    if (reset==true){
        return;
    }
    
    reset_button.disabled = true;
    if(orientation === "black"){
        [isgameover, turn] = await GET_engine_move();
    }
    reset_button.disabled = false;

}

function set_names(){
    let opponent_title = "PRL Self-Trained Model"
    if (opponent === "datatrain_model.h5"){
        opponent_title = "PRL Data-Trained Model";
    }
    else if (opponent === "combined_model.h5"){
        opponent_title = "PRL Combined Model";
    }
    player1.innerHTML = opponent_title;
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
        if(m>1){
            mins.innerHTML = "0" + (mins.innerHTML - 1);
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
            
            if(color === "white"){
                history.innerHTML = history.innerHTML.concat("<br> <b>White out of time. Black Wins!</b>")
                scrollbox.scrollTop = scrollbox.scrollHeight;
            }
            else if(color === "black"){
                history.innerHTML = history.innerHTML.concat("<br> <b>Black out of time. White Wins!</b>")
                scrollbox.scrollTop = scrollbox.scrollHeight;
            }
            
            isgameover = true;
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
            minutes.innerHTML = "0" + parseInt(minutes.innerHTML) + 1;
        } 
        else{
            minutes.innerHTML = parseInt(minutes.innerHTML) + 1;
        }
        seconds.innerHTML = "0" + parseInt(diff);
    }
}













