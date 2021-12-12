# Python Chess Engine

This project is about three chess engines (Python Machine Learning Chess Engine) based
on machine learning, and more specifically on reinforcement and supervised learning, as
well as an online application that allows the user to play against the chess engines, 
but also to watch them play against each other. The chess engines were 
developed using Python programming language. In total, three different game models 
were created, a model that was trained by playing games against itself, a model that 
was trained with data from past professional games stored in online databases and a 
combinational model that was trained using both methods. The engines’ choice of 
move is made using Monte Carlo Tree Search, which is a heuristic algorithm for certain 
types of decision-making processes. In addition, a web application was created that 
allows the user to play against the engines, but also to watch the engines play against 
each other. The results highlight the usefulness of machine learning in complex 
problems, without any prior knowledge of the strategy and characteristics of the 
problem, but also without the need for human analysis of their parameters.

![image](https://user-images.githubusercontent.com/49875599/145675570-969eac87-68ab-4f64-8454-abecd16632c6.png)

Two different neural network model types were created for the project, combining deep neural networks with convolutional neural networks. The first one is about position evaluation, whereas the other one is about probabilistic move prediction for a given position. The models were created using the Keras API. In total, six models were created, two for each engine. 
    
![image](https://user-images.githubusercontent.com/49875599/145676850-f391190f-04d1-4cd0-a61c-4cf0f42849ca.png)


Monte Carlo tree search was used to analyze the game tree and decide which is the best move, while using both neural network models. Selection process is based on a variation of the UCB1 method, making use of the move prediction network. Simulation process is replaced by the evaluation network. Parameters were set experimentally. The search process is accelerated using NVIDIA GeForce GTX 1660 Ti with Max-Q Design GPU, which supports CUDA design, a parallel programming platform created by NVIDIA. The library cuDNN was also utilized using the tensorflow-gpu python library.
    
![image](https://user-images.githubusercontent.com/49875599/145676868-8f3d0496-98c9-4641-ab9c-f64ff2941725.png)
    
Chess engines ELO were estimated at around 1300-1450, after facing off different versions of the Stockfish chess engine on lichess.com. 
    
    
Apart from the chess engines, a website was created for the purpose of giving the user the opportunity to play against them or watch them play against each other. The website was created using, Python (Flask API), HTML5, CSS and Javascript.
    
![image](https://user-images.githubusercontent.com/49875599/145676991-fd876ab5-1eef-40bc-ab0a-49a663dba9ca.png)
   
![image](https://user-images.githubusercontent.com/49875599/145677007-ddbf0789-00dd-4b2d-81a0-34db2a1711ee.png)

![image](https://user-images.githubusercontent.com/49875599/145677011-7cc6884d-1499-41da-8564-a323de31429f.png)

![image](https://user-images.githubusercontent.com/49875599/145677019-607a8486-275f-4877-a561-10bafe424f7c.png)
