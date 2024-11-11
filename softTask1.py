import random

def parse_test_cases(file_path):
    test_cases = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_cases = int(lines[0].strip())  

        line_index = 1  
        for _ in range(num_cases):
            max_time = int(lines[line_index].strip())  
            num_tasks = int(lines[line_index + 1].strip())  
            tasks = [int(lines[line_index + 2 + i].strip()) for i in range(num_tasks)]  # List of tasks
            
            chromosome_length = num_tasks 
            
            test_cases[max_time] = {'tasks': tasks, 'chromosome_length': chromosome_length}
            
            line_index += 2 + num_tasks  

    return test_cases

file_path = "soft.txt"
test_cases_dict = parse_test_cases(file_path)

chromosome= list[bin]
chromosome_length= 5
population = list[chromosome]
task_times= [10,20,30,40,50]

def rand_genome(chromosome_length):
    return [random.randint(0,1) for _ in range(chromosome_length)]


def fitness(task_times,chromosome):
    core1_time= sum(task_times[i] for i in range(len(chromosome)) if chromosome[i]==1)
    core2_time= sum(task_times[i] for i in range(len(chromosome)) if chromosome[i]==0)

    return max(core1_time,core2_time)
def init_pop(population_size:int,genome_length,max_time):
    population=[]
    while len(population)<population_size:
        chromosome=rand_genome(genome_length)
        if fitness(task_times,chromosome) <=max_time:
            population.append(chromosome)
            
    return population
def crossover(parent1,parent2):
    crossover_probability = random.uniform(0.4,0.7)
    crossover_point = random.randint(1,len(parent1)-1)
    if random.random() < crossover_probability:
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent1[crossover_point:] + parent2[:crossover_point]
        return offspring1,offspring2
    else:
        return parent1,parent2

def mutate(chromosome):
    mutation_probability = 0.05 
    for i in range(len(chromosome)):
        if random.random() < mutation_probability:
            chromosome[i] = 1 if chromosome[i] == 0 else 0
    return chromosome
def elitism_replacement(population, task_times):
    fitness_values = [(chromosome, fitness(task_times, chromosome)) for chromosome in population]
    
    sorted_population = sorted(fitness_values, key=lambda x: x[1], reverse=False)
    
    sorted_chromosomes = [chromosome for chromosome, _ in sorted_population]
    top_two_chromosomes = sorted_chromosomes[:2]
        
    final_population = top_two_chromosomes + sorted_chromosomes[2:]
    
    return final_population


def wheel_selection(population,fscores):
    total_score=sum(fscores)

    relative_fitness=[ fitness/total_score for fitness in fscores]

    commulative_score = 0
    commulative_fitness= []
    for r_score in relative_fitness:
        commulative_score += r_score
        commulative_fitness.append(commulative_score)

    selected_parents = []
    
    for _ in range(2):
        random_no= random.random()
        for i, commulative_value in enumerate(commulative_fitness):
            if random_no <= commulative_value:
                selected_parents.append(population[i])
                break
    

    return selected_parents
def genAlgo(task_times,chromosome_length, generations=1000, pop_size=50):
    population = init_pop(pop_size, chromosome_length, 100)
    
    newpop = elitism_replacement(population, task_times)
    for _ in range(len(newpop)):
        print(fitness(task_times, newpop[_]), end=" ")
    
    i = 0
    while i < generations:
        i += 1
        for j in range(2, len(newpop) // 2 + 2):
            parents = wheel_selection(newpop, [fitness(task_times, _) for _ in newpop])
            
            newpop.pop(j)  
            newpop.pop(j)  
            
            offspring = crossover(parents[0], parents[1])
            offspring = list(offspring)
            
            offspring[0] = mutate(offspring[0])
            offspring[1] = mutate(offspring[1])
            
            newpop.append(offspring[0])
            newpop.append(offspring[1])
        
        newpop = elitism_replacement(newpop, task_times)
    
    return newpop

for max_time, data in test_cases_dict.items():
    tasks = data['tasks']
    chromosome_length = data['chromosome_length']
    print(f"Running genAlgo for test case with max time {max_time}, tasks {tasks}, chromosome length {chromosome_length}")
    final_population = genAlgo(tasks, chromosome_length)
    top_chromosome = final_population[0]
    print(f"Final Population: {final_population}\n")
    if fitness(tasks,top_chromosome)<=max_time:
        print("Top candidate is ",fitness(tasks,top_chromosome))
    else:
        print("Top candidate is not feasible")
