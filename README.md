# [FIRST PROJECT] Artificial Intelligence

## Summary

This is basically a graph search problem where you can have different types of paths to nodes (taxi, bus, subway) and different agents should all arrive the their respective destinations at the same time.  
The following image was the map used in the evaluation  
![alt text](https://github.com/Rickerp/IST-IA-P1/blob/master/maps.png)

## Objective

When given something like this  
```
SP = SearchProblem(goal = [63,61,70], model = U, auxheur=coords)
I = [30,40,109]
nn = SP.search(I,limitexp = 3000, limitdepth = 10, tickets = [5,20,2])
```
where 
* `goal` are the endpoints of each agent  
* `model` is the map formatted  
* `auxheur` are the coordinates of each node position formatted  
* `I` are the starting points of each agent  
* `limitexp` max number of expansions
* `limitdepth` max depth
* `tickets` number of times you can use each type of path `[subway, taxi, bus]`  

(Note: An example of model and auxheur can be seen using `model = pickle.load(open("graph.pickle", "rb"))[1]` and `auxheur = pickle.load(open("coords.pickle", "rb"))`. Check ![sol_verify.py](https://github.com/Rickerp/IST-IA-P1/blob/master/sol_verify.py) for more info)

the answer should be something like this
```
[[[], [30, 40, 109]], [[2, 0, 1], [69, 41, 84]], [[0, 0, 1], [63, 42, 61]], [[0,
1, 1], [69, 60, 84]], [[1, 1, 0], [63, 61, 70]]]
```
where, for example, looking at `[[2, 0, 1], [69, 41, 84]]`:  
* The first agent used the subway(2) to get to node 69
* The second agent used a taxi(0) to get to node 41
* The third agent used the bus(1) to get to node 84

## Solution

The solution implemented is based on [Iterative deepening A* (IDA*)](https://en.wikipedia.org/wiki/Iterative_deepening_A*) 

## Check ![project.pdf](https://github.com/Rickerp/IST-IA-P1/blob/master/assets/project.pdf) for more detailed info (in portuguese)

## Running
1. Import main file `import main`  
2. Run like in example above  

## Authors 
| Name | University | More info |
| ---- | ---- | ---- |
| Ricardo Fernandes | Instituto Superior Técnico | [<img src="https://i.ibb.co/brG8fnX/mail-6.png" width="17">](mailto:ricardo.s.fernandes@tecnico.ulisboa.pt "ricardo.s.fernandes@tecnico.ulisboa.pt") [<img src="https://github.githubassets.com/favicon.ico" width="17">](https://github.com/rickerp "rickerp") [<img src="https://i.ibb.co/TvQPw7N/linkedin-logo.png" width="17">](https://www.linkedin.com/in/rickerp/ "rickerp") |
| Rafael Galhoz | Instituto Superior Técnico | [<img src="https://i.ibb.co/brG8fnX/mail-6.png" width="17">](mailto:rafael.galhoz@tecnico.ulisboa.pt "rafael.galhoz@tecnico.ulisboa.pt") [<img src="https://github.githubassets.com/favicon.ico" width="17">](https://github.com/VivaRafael "VivaRafael") [<img src="https://i.ibb.co/TvQPw7N/linkedin-logo.png" width="17">](https://www.linkedin.com/in/rafael-galhoz/ "rafael-galhoz") |
