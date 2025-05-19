
import json
import evo_algo

import matplotlib.pyplot as plt

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend



# Run this file to produce graphs from a run

path_result_json = "result.json"

def get_results(path_results: str):
     with open(path_results, 'r') as file:
        results_dict = json.load(file)   
        return results_dict

    
def get_best_individual(path_results: str):
     best_itr = 0
     best_ind_i = 0
     best_fitness = 10000
     best_config = None
     with open(path_results, 'r') as file:
          results_dict = json.load(file)
          # Loop through keys and values
          for i in range( len( results_dict.keys() ) ):
               for j in range( len( results_dict[ f"itr_{i}" ]["individuals"] ) ):
                    # if "step_101" not in results_dict[f"itr_{i}"]["individuals"][j]["stats"]: continue
                    if results_dict[f"itr_{i}"]["individuals"][j]["fitness"] < best_fitness:
                         best_fitness = results_dict[f"itr_{i}"]["individuals"][j]["fitness"]
                         best_ind_i = j
                         best_itr = i
                         best_config = results_dict[f"itr_{i}"]["individuals"][j]["config"]
     print(best_config)
     return best_itr, best_ind_i, best_fitness



def get_worst_individual(path_results: str):
     worst_itr = 0
     worst_ind_i = 0
     worst_fitness = 0
     with open(path_results, 'r') as file:
          results_dict = json.load(file)
          # Loop through keys and values
          for i in range( len( results_dict.keys() ) ):
               for j in range( len( results_dict[ f"itr_{i}" ]["individuals"] ) ):
                    # if "step_101" not in results_dict[f"itr_{i}"]["individuals"][j]["stats"]: continue
                    if results_dict[f"itr_{i}"]["individuals"][j]["fitness"] > worst_fitness:
                         worst_fitness = results_dict[f"itr_{i}"]["individuals"][j]["fitness"]
                         worst_ind_i = j
                         worst_itr = i
     return worst_itr, worst_ind_i, worst_fitness




def make_graph_of_individual_run(itr: int, ind_i: int, fitness: int, path_results: str, filename: str):

    results_dict = get_results(path_results)

    ind_config = results_dict[f"itr_{itr}"]["individuals"][ind_i]["config"]
    ind_stats = results_dict[f"itr_{itr}"]["individuals"][ind_i]["stats"]

    # Initialize lists to store the values
    days = []
    deaths = []
    critical = []
    vaccinated = []
    hospitalized = []
    recovered = []
    symptomatic = []

    sum_deaths = results_dict[f"itr_{itr}"]["individuals"][ind_i]["stats"]["sum_deaths"]
    sum_symptometic = results_dict[f"itr_{itr}"]["individuals"][ind_i]["stats"]["sum_symptometic"]
    
    # Populate the lists from each step
    for i in range(evo_algo.ITERATIONS_INDIVIDUAL):
        step = ind_stats[f"step_{i}"]
        days.append(i + 1)
        deaths.append(step["deaths"])
        critical.append(step["critical"])
        vaccinated.append(step["vaccinated"])
        hospitalized.append(step["hospitelized"])
        recovered.append(step["recovered"])
        symptomatic.append(step["symptometic"])

    # Plot each value
    plt.figure(figsize=(10, 6))
    plt.plot(days, deaths, label="Deaths", linestyle='-', marker='o')
    plt.plot(days, critical, label="Critical", linestyle='-', marker='o')
    plt.plot(days, vaccinated, label="Vaccinated", linestyle='-', marker='o')
    plt.plot(days, hospitalized, label="Hospitalized", linestyle='-', marker='o')
    plt.plot(days, recovered, label="Recovered", linestyle='-', marker='o')
    plt.plot(days, symptomatic, label="Symptomatic", linestyle='-', marker='o')
    
    # Labeling
    # individual index: {ind_i}
    plt.title(f"Generation: {itr} Individual in generation: {ind_i}, Fitness: {fitness}, Deaths: {sum_deaths}, Infected: {sum_symptometic}")
    plt.xlabel("Days")
    plt.ylabel("Number of Individuals")
    plt.legend()
    plt.grid(True)

    plt.savefig(filename)



def plot_best_individual_at_each_generation(results_path):
     results = get_results(results_path)

     best_itrs = []
     best_ind_is = []
     best_fitnesses = []
     for i in range( len( results.keys() ) ):
          best_fitness = 1000
          best_itr = 0
          best_ind_i = 0
          print(f"gen: {i}, ")
          for j in range( len( results[ f"itr_{i}" ]["individuals"] ) ):
               print(f" {results[f"itr_{i}"]["individuals"][j]["fitness"]},", end=" " )
               if results[f"itr_{i}"]["individuals"][j]["fitness"] < best_fitness:
                    best_fitness = results[f"itr_{i}"]["individuals"][j]["fitness"]
                    best_itr = i
                    best_ind_i = j
          best_itrs.append(best_itr)
          best_ind_is.append(best_ind_i)
          best_fitnesses.append(best_fitness)

     
     for i in range(len(best_itrs)):
          make_graph_of_individual_run(best_itrs[i], best_ind_is[i], best_fitnesses[i], results_path, f"best_ind_gen_{i}.png")
     








     

def plot_hyperparameters_over_time(path_results):
    gen_fitnesses, gen_configs = get_hyperparameters_over_time(path_results)
    parameters = ["new_vaccines", "new_patients", "m", "cd"]

    # Loop through each parameter and create a separate plot
    for param in parameters:
        plt.figure(figsize=(10, 6))

        # Prepare x-axis labels with average fitness
        x_labels = []
        
        for gen_idx, configs in enumerate(gen_configs):
            if len(gen_fitnesses[gen_idx]) > 0:
                # Calculate average and best fitness
                avg_fitness = sum(gen_fitnesses[gen_idx]) / len(gen_fitnesses[gen_idx])
                best_fitness = min(gen_fitnesses[gen_idx])
                best_index = gen_fitnesses[gen_idx].index(best_fitness)
                
                # Collect x-labels as "Gen X\nAvg: Y"
                x_labels.append(f"{gen_idx}\nAvg: {avg_fitness:.2f}")
                
                # Get the parameter values for this generation
                values = [config[param] for config in configs]

                # Scatter plot all values for that parameter at the same x index
                plt.scatter([gen_idx] * len(values), values, alpha=0.6)

                # Plot the best one in red
                plt.scatter(gen_idx, values[best_index], color='red', edgecolor='black', label='Best Fitness' if gen_idx == 0 else "")
            else:
                x_labels.append(f"{gen_idx}\nAvg: N/A")

        # Update the x-axis with new labels
        plt.xticks(range(len(gen_configs)), x_labels, rotation=45, ha='right')
        
        plt.title(f"Parameter: {param}")
        plt.xlabel("Generation\n(Avg Fitness)")
        plt.ylabel("Value")
        plt.grid(True)
        plt.legend()

        # Save each plot separately
        output_filename = f"hyperparameters_{param}.png"
        plt.tight_layout()
        plt.savefig(output_filename, dpi=300)
        plt.close()
        print(f"Plot for '{param}' saved as '{output_filename}'")


     
def get_hyperparameters_over_time(path_results):
    results = get_results(path_results)

    gen_fitnesses = []
    gen_configs = []
    for i in range( len( results.keys() ) ):
         fitnesses = []
         configs = []
         for j in range( len( results[ f"itr_{i}" ]["individuals"] ) ):
              config = results[f"itr_{i}"]["individuals"][j]["config"]
              fitness = results[f"itr_{i}"]["individuals"][j]["fitness"]
              configs.append( config )
              fitnesses.append( fitness )
         gen_configs.append( configs )
         gen_fitnesses.append( fitnesses )
    return gen_fitnesses, gen_configs





itr, ind_i, fitness = get_best_individual(path_result_json)
make_graph_of_individual_run(itr, ind_i, fitness, path_result_json, "best_run.png")

itr, ind_i, fitness = get_worst_individual(path_result_json)
make_graph_of_individual_run(itr, ind_i, fitness, path_result_json, "worst_run.png")




plot_hyperparameters_over_time(path_result_json)





plot_best_individual_at_each_generation(path_result_json)





"""
evolution = {
    "itr_1": {
        "indivudials": [
            {
                "config": None, # config fila med parametere
                "stats": None, # statistikk
                "fitness": 0
            }
        ]
    }
}
"""











