let starting_fen = document.getElementById("starting_fen").innerHTML;
let first_legal_moves = document.getElementById("first_moves").innerHTML
                  .replace("[","").replace("]","").replace(/'/gi, "").split(", ");
                  
let legal_moves = first_legal_moves;
let isgameover = false;
let turn = true;
let reset = false;
let orientation = "white";

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


function reset_board(){
   reset = true;
   board.position(starting_fen)
   isgameover = false;
   turn = true;
   
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
    legal_moves = first_legal_moves;
}

function onDragStart(source, piece, position, orientation){

    if(isgameover === true){
        return false}
    if((orientation === "white" && piece.search(/^w/) === -1) ||
       (orientation === "black" && piece.search(/^b/) === -1)){
        return false
    }
}

function onDrop(source, target, piece, newPos, oldPos, orientation){
    
    removeGreySquares();
    
    let move = source.concat(target);
    
    if(orientation === "white" && piece.search(/P/) === 1 && target.search(/8/) === 1){
        move = move + 'q';
        console.log(move);
    }
    if(!legal_moves.includes(move) || isgameover || !turn){
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
            turn = false;
    })
    
    GET_data();
    
}

async function GET_data(){

    [isgameover, turn] = await GET_board();
    
    if(isgameover===false){
        [isgameover, turn] = await GET_engine_move();
    }
    
    if(isgameover===true){
        GET_result();
    }
}

function onMouseoverSquare (square, piece) {
  
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
    
    await fetch('/get_player_move')
        .then(async function (response) {         
            return await response.json();
        }).then(function (text) {
            if(text.isgameover == false){
                board.position(text.fen)
                console.log('GET response:');
                console.log(text.move); 
                console.log(text.player); 
                console.log(text.fen);
                console.log(text.isgameover)
            }
        
        isgameover = text.isgameover;
        turn = false;

    });
    
    return [isgameover, turn] ;
    
}

async function GET_engine_move(){

    
    await fetch('/get_engine_move')
         .then(async function (response) {         
             return response.json();
         }).then(await function (text) {
             if(text.isgameover == false){
                 board.position(text.fen)
                 console.log('GET response:');
                 console.log(text.move); 
                 console.log(text.player); 
                 console.log(text.fen);
                 console.log(text.isgameover)
             }
             
             isgameover = text.isgameover;
             legal_moves = text.legal_moves;
             turn = true;
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
        });
        
    return;
        
}














