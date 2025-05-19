



def compute_fitness(stats):
    return 2 * stats["sum_deaths"] + stats["sum_symptometic"]


def initilize_body(config, stats):
    fitness = compute_fitness(stats)
    return {
        "config": config,
        "stats": stats,
        "fitness": fitness
    }


def add_individual_at_itr(itr: int, body, evolution):
    evolution[f"itr_{itr}"]["individuals"].append( body )
    return evolution


def add_itr(evolution, new_itr: int):
    evolution[f"itr_{new_itr}"] = {"individuals": []}
    return evolution


def init_evolution_stats():
    evolution = {}
    evolution = add_itr(evolution, 0)
    return evolution




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


