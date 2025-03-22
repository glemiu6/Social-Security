# The Problem of Social Security Sustainability.

### A Run Down About The Structure Of The Projects:
Let's very simply imagine that we have a certain amount accumulated in a pension fund. We have a population structured into 2 genders (Male and Female) and 3 categories (Young, Adult, Old). Young people have no salary or pension, Adults receive a salary, Old people receive a pension. Then there are population dynamics.  
People die, a process simulated by a probability that varies according to age. (For automatic evaluation, we will not use randomness, we have a process that simulates this in a deterministically way.) People are also born as a result of interactions between male and female people (can you say that?).  
<hr>

### Tasks:

#### READ DATA
1. We made a function `ler_config(S)` that reads a file names `config_S.txt`, where `S` is the code of the simulation. The function should return a dictionary where the keys are the names of the constances that will be used throughout the code.
2. The function `nova_pessoa(idade=0)` return a dictionary with the detailes of the people(id,name,gender -> if the id is a even number "M" else "F", age,salary that will be 1000,pension that will be 500).
3. Now we read the population with the function `ler_populacao_inicia(S)` where the `S` is a code and opens the file `população_inicial_S.txt` and return a population represented by a list of people.  

P.S: The data for the reading is on the directory named : `files`


#### MAKE THE SIMULATION
1. Create the function `exclude_entities(entidades, percentagem, ano_corrente)` that receives a list of enteties , a percent and a year and should return a percentage p of entities deterministically based on the year.
2. Make a function `simula_ano(populacao, ano_corrente)` , that simulates the year one by one. Should receive a population(list) , a year and should return a new population(this new population is the population that has survived and didn't reach the age limit and the ones that were born). Each category has it's own mortality rate.Wwe also need to create a person according to the birth rate(use the function `nova_pessoa(idade=0)`).
3. Now we create a function `cobra_seg_social(year,funds,population)` makes the collection and the payments from the population and return a new pension fund. The youngs don't pay or get paid, the adults give a percent from their salary that is defined in `config_S.txt` and the older people get paid from the fund .


#### SIMULATE DIFFERENT YEAR:
Make a program that given the population read and the parameters, generate the number of years needed, simulates the years starting from `ANO_INICIAL`. The population should be changed after the years and the pension fund.  
At the start of the program should be printed :  
`A simulação começou no ano A, com população total de P, e o fundo de pensões a valer V.`  
If the pension funds geys to a negative number , the program should print:  
`No ano B, a população foi P e o fundo de pensões foi negativo, com valor W.`  
And at the end, the program should print:  
`A simulação terminou no ano C, com população total de K pessoas e o fundo de pensões vale Z.`  
The program should also create a file were the final population is represented with the name `população_final_S.txt` ,where `S` is the code for the simulation. 