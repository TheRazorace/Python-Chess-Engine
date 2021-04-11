let starting_fen = document.getElementById("starting_fen").innerHTML;

let board = ChessBoard('board', {
   position: starting_fen,
   draggable: true,
   showNotation: true,
   moveSpeed: 'fast',
   snapbackSpeed: 500,
   snapSpeed: 100
});

let reset = false;
function reset_board(){
   reset = true;
   board.position('start')
   
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
}

let isgameover = false;

async function fetch_move(){   
    reset = false; 
    isgameover = false;
     
    while(isgameover==false){
         if(reset==true){
             board.position('start')
             return;
         }
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
                 }
             
             isgameover = text.isgameover;

          });
    }  
    
    await fetch('/selfmove')
         .then(async function (response) {         
             return await response.json();
         }).then(function (text) {
             console.log('GET response:');
             console.log(text.result);  
             console.log(text.msg);
    });
}

