import streamlit as st
import random
import time

st.set_page_config(
    page_title="Genetic Algorithm"
)

st.header("Genetic Algorithm", divider="gray")

#POP_SIZE: Number of Chromosomes in our list.
POP_SIZE = 500
#POP_SIZE = st.number_input("Enter population size")

#MUT_RATE: Rate at which our string will be changed.
#MUT_RATE = 0.2

#TARGET: Our goal.
#TARGET = 'fakhitah'
    

#GENES: Options from which our population would be created.
GENES = ' abcdefghijklmnopqrstuvwxyz'

#initialization

def initialize_pop(TARGET):
  population = list()
  tar_len = len(TARGET)

  for i in range(POP_SIZE):
      temp = list()
      for j in range(tar_len):
          temp.append(random.choice(GENES))
      population.append(temp)

  return population

#fitness calculation
#0 fitness means target found

def fitness_cal(TARGET, chromo_from_pop):
  difference = 0
  for tar_char, chromo_char in zip(TARGET, chromo_from_pop):
      if tar_char != chromo_char:
          difference+=1
  return [chromo_from_pop, difference]

#selection
#returns top 50% population sorted according to fitness

def selection(population, TARGET):
  sorted_chromo_pop = sorted(population, key= lambda x: x[1])
  return sorted_chromo_pop[:int(0.5*POP_SIZE)]

#crossover

def crossover(selected_chromo, CHROMO_LEN, population):
  offspring_cross = []
  for i in range(int(POP_SIZE)):
    parent1 = random.choice(selected_chromo)
    parent2 = random.choice(population[:int(POP_SIZE*50)])

    p1 = parent1[0]
    p2 = parent2[0]

    crossover_point = random.randint(1, CHROMO_LEN-1)
    child =  p1[:crossover_point] + p2[crossover_point:]
    offspring_cross.extend([child])
  return offspring_cross

#mutation

def mutate(offspring, MUT_RATE):
  mutated_offspring = []

  for arr in offspring:
      for i in range(len(arr)):
          if random.random() < MUT_RATE:
              arr[i] = random.choice(GENES)
      mutated_offspring.append(arr)
  return mutated_offspring

#replacement

def replace(new_gen, population):
  for _ in range(len(population)):
      if population[_][1] > new_gen[_][1]:
        population[_][0] = new_gen[_][0]
        population[_][1] = new_gen[_][1]
  return population

#main

def main(POP_SIZE, MUT_RATE, TARGET, GENES):
    # 1) initialize population
    initial_population = initialize_pop(TARGET)
    found = False
    population = []
    generation = 1

    # 2) Calculating the fitness for the current population
    for _ in range(len(initial_population)):
        population.append(fitness_cal(TARGET, initial_population[_]))

    # now population has 2 things, [chromosome, fitness]
    # 3) now we loop until TARGET is found
    while not found:

      # 3.1) select best people from current population
      selected = selection(population, TARGET)

      # 3.2) mate parents to make new generation
      population = sorted(population, key= lambda x:x[1])
      crossovered = crossover(selected, len(TARGET), population)

      # 3.3) mutating the children to diversify the new generation
      mutated = mutate(crossovered, MUT_RATE)

      new_gen = []
      for _ in mutated:
          new_gen.append(fitness_cal(TARGET, _))

      # 3.4) replacement of bad population with new generation
      # we sort here first to compare the least fit population with the most fit new_gen

      population = replace(new_gen, population)


      if (population[0][1] == 0):
        st.write('Target found')
        st.write('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(population[0][1]))
        break
      st.write('String: ' + str(population[0][0]) + ' Generation: ' + str(generation) + ' Fitness: ' + str(population[0][1]))
      generation+=1
        
with st.form("my_form"):
    TARGET = st.text_input("Enter your name")
    MUT_RATE = st.number_input("Enter your mutation rate")

    calculate = st.form_submit_button("Calculate")

    if calculate:
        main(POP_SIZE, MUT_RATE, TARGET, GENES)




