import pycxsimulator
from pylab import *
import copy as cp
import uuid
from random import random, sample
from pprint import pprint
from mutation import *
from grupper import get_risikogrupper, get_sum_n
from agent import *
from config import get_config

import evo_algo
import evo_metrics

import warnings


warnings.filterwarnings("ignore", message=".*marker is redundantly defined.*")


import warnings
from matplotlib import MatplotlibDeprecationWarning

warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)




gui = pycxsimulator.GUI()
config = get_config()
grupper = get_risikogrupper()
iteration = 0

# number of agents
n = get_sum_n()
if config["ns"] > n:
    raise Exception(f"sick population of {config['ns']} is larger than total population {n}")

# initilize statistics
stats = init_stats()





def initialize():
    global agents, stats, first_uuid, n, grupper, iteration
    
   
    agents = []
    total_agents = n
    
    # Create all agents initially not sick
    for key in grupper:
        for i in range(grupper[key]["n"]):
            ag = agent(
                sick=False,
                x=random(),
                y=random(),
                gruppe=key
            )
            agents.append(ag)
    
    ns = min(config["ns"], total_agents)
    
    # Get indices of agents to infect, so we modify the list directly
    sick_indices = sample(range(total_agents), ns)
    
    
    # Set agents as sick by index
    for idx in sick_indices:
        agents[idx].sick = True
        stats[f"step_{iteration}"]["symptometic"] += 1
        stats["sum_symptometic"] += 1

            
            
def observe():
    global agents, grupper
    cla()
    
    alive = [ag for ag in agents if ag.dead == False]

    sicks = [ag for ag in alive if ag.sick]

    with warnings.catch_warnings(record=True) as w:
        if len(sicks) > 0:
            x = [ag.x for ag in sicks]
            y = [ag.y for ag in sicks]
            plot(x, y, config["c"], marker='o', linestyle='')

        healthies = [ag for ag in alive if ag.sick == False]
        for key in grupper:
            x = [ag.x for ag in healthies if ag.gruppe == key]
            y = [ag.y for ag in healthies if ag.gruppe == key]
            plot(x, y, color=grupper[key]['c'], marker='o', linestyle='')

        deads = [ag for ag in agents if ag.dead]
        if len(deads) > 0:
            x = [ag.x for ag in deads]
            y = [ag.y for ag in deads]
            plot(x, y, color=config["dead_color"], marker='o', linestyle='')

        axis('image')
        axis([0, 1, 0, 1])
    for warning in w:
        pass



def update_one_agent(vaccines_t, patients_t):
    global agents,stats, grupper, n, iteration
    if agents == []:
        return vaccines_t, patients_t

    ag = choice(agents)

    
    if ag.dead: return vaccines_t, patients_t # dont update if agent is dead
    
    ag.x += uniform(-config["m"], config["m"])
    ag.y += uniform(-config["m"], config["m"])
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # infection ceases
    if ag.symptometic_t == config["sick_t_max"] and ag.critical == False:
        ag.sick = False
        ag.immune = True
        stats["sum_recovered"] += 1
        stats[f"step_{iteration}"]["symptometic"] -= 1
        stats[f"step_{iteration}"]["recovered"] += 1
        ag.symptometic_t = 0

    # dies from infection
    if ag.critical_t == config["critical_t_max"] and ag.critical:
        ag.dead = True
        stats['sum_deaths'] += 1
        stats[f"step_{iteration}"]["deaths"] += 1
        stats[f"step_{iteration}"]["symptometic"] -= 1
        stats[f"step_{iteration}"]["critical"] -= 1
        return vaccines_t, patients_t

    # takes vaccine
    if (ag.immune == False and config["new_vaccines"]/n) > random() and vaccines_t > 0: # sannsynlighet for å få vaksine
        ag.immune = True
        vaccines_t -= 1
        stats["sum_vaccinated"] += 1
        stats[f"step_{iteration}"]["vaccinated"] += 1

    # hospitelized
    if ag.critical and config["new_patients"]/n > random() and patients_t > 0:
        ag.critical = False
        ag.sick = False
        ag.immune = True
        ag.critical_t = 0
        patients_t -= 1

        stats[f"step_{iteration}"]["symptometic"] -= 1
        stats[f"step_{iteration}"]["recovered"] += 1
        stats[f"step_{iteration}"]["critical"] -= 1
        stats[f"step_{iteration}"]["hospitelized"] += 1
        stats["sum_hospitelized"] += 1
        stats["sum_recovered"] += 1

    # comes in critical condition
    if ag.gruppe != "ingen_risiko" and ag.sick and ag.critical == False and (config["pc"] > random()):
        # pprint(stats)
        ag.critical = True
        stats[f"step_{iteration}"]["critical"] += 1
        stats["sum_critical"] += 1
        
        
    # becomes infected
    if ag.sick == False and ag.immune == False:
        # infected neighbours
        neighbors = [
                    nb for nb in agents
                    if (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < config["cdsq"] and # person er i nærheten 
                    nb.sick and 
                    nb.dead == False 
                    ]

        # if a neighbour is infected, infect agent
        if len(neighbors) > 0:
            ag.sick = True
            ag.immune = True
            stats["sum_symptometic"] += 1
            stats[f"step_{iteration}"]["symptometic"] += 1
            
    # update critical rounds
    if ag.critical:
        ag.critical_t += 1

    # update infected rounds
    if ag.sick and ag.critical_t == 0:
        ag.symptometic_t += 1
    return vaccines_t, patients_t



def update():
    global agents, iteration, stats
    t = 0.
    vaccines_t = config["new_vaccines"]
    patients_t = config["new_patients"]
    while t < 1. and len(agents) > 0:
        t += 1. / len(agents)
        vaccines_t, patients_t = update_one_agent(vaccines_t, patients_t)
    if iteration == evo_algo.ITERATIONS_INDIVIDUAL:
        gui.quitGUI()
    iteration += 1
    # update statistics
    stats[f"step_{iteration}"] = stats[f"step_{iteration-1}"].copy()
    stats[f"step_{iteration}"]["hospitelized"] = 0
    stats[f"step_{iteration}"]["deaths"] = 0
    stats[f"step_{iteration}"]["vaccinated"] = 0 

    

def add_standard_body_to_ind(standard_body, individual_body):
    for key, value in standard_body.items():
        if key not in individual_body:
            individual_body[key] = value
    return individual_body



def assemble_scores(evo_stats, itr):
    bodies = evo_stats[f"itr_{itr}"]["individuals"]
    scores = []
    for body in bodies:
        scores.append( body["fitness"] )
    return scores

evo_stats = evo_metrics.init_evolution_stats()
itr = 0

standard_body = get_config()
individual_configs = []
# INITILIZE INDIVIDUALS RANDOMLY
for i in range( evo_algo.POPULATION_SIZE ):
    individual_body = evo_algo.initialize_individual()
    ind_config = add_standard_body_to_ind(standard_body, individual_body)
    individual_configs.append( ind_config )



def try_config(new_vaccines: int, new_patients: int, m: float, cd: float):
    global config
    ind = {
        "new_vaccines": new_vaccines,
        "new_patients": new_patients,
        "m": m,
        "cd": cd,
    }
    ind["cdsq"] = round(ind["cd"] ** 2, 6)
    ind_config = add_standard_body_to_ind(standard_body, individual_body)

    config = ind_config
    gui.start(func=[initialize, observe, update])
    sys.exit()



# EVOLUTION
for i in range( evo_algo.NUM_GENERATIONS ):
    # RUN SIMULATION FOR EACH INDIVIDUAL
    for ind_config in individual_configs:
        # INITILIZE STATS AND CONFIG FOR INDIVIDUAL
        s_stats = init_stats()
        stats = s_stats
        config = ind_config
        # RUN SIMULATION, WHICH WILL WRITE STATS FOR INDIVIDUAL DURING RUNG

        try:
           with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                gui = pycxsimulator.GUI()
                gui.start(func=[initialize, observe, update])
                for warning in w:
                    print(f"Warning caught: {warning.message}")
        except tkinter.TclError as tk_err:
            print(f"TclError ignored: {tk_err}")
        except Exception as ex:
            print(ex)

        iteration = 0 # reset iteration
        # MAKE A BODY FROM THE STATS REPRESENTING AN INDIVIDUAL
        body = evo_metrics.initilize_body(ind_config, stats)
        evo_stats = evo_metrics.add_individual_at_itr(itr, body, evo_stats)
    # INITILIZE NEW INDIVIDUALS BASED ON PREVIOUS GENERATION
    individual_configs = []
    scores = assemble_scores(evo_stats, itr)
    for i in range( evo_algo.POPULATION_SIZE ):
        # parent selection
        parent1, parent2 = evo_algo.select_parents( evo_stats[f"itr_{itr}"]["individuals"] , scores)
        # crossover
        child_config = evo_algo.crossover(parent1["config"], parent2["config"])
        # mutation
        child_config = evo_algo.mutate(child_config)
        child_config_with_standard = add_standard_body_to_ind(standard_body, child_config)
        individual_configs.append( child_config_with_standard.copy() )
        
    # MARK NEXT GENERATION
    itr += 1
    evo_stats = evo_metrics.add_itr(evo_stats, itr)
    print("genertion: ", itr)



    
import json

# save statistics
path_result_json = "project/result.json"
with open(path_result_json, "w") as file:
    json.dump(evo_stats, file, indent=4)

print("DONE WITH RUNNING SIM")


