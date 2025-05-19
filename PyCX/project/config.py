

def get_config():
    return {
        "dead_color": "#000000", # color of dead agents 
        "c": 'ro', # color of sick agents

        "ns": 12, # initial sick population, basert på 20% av befolkninga

        "pc": 0.1, # likelyhood to become in critical condition, if risikogruppe
        "pc_no": 0.01, # likelyhood to become critical condition, if no risikogruppe
               
        "sick_t_max": 30, # turns sickness lasts
        "critical_t_max": 30, # mengde tid man er i kritisk kondisjon, før man dør

        # parametere for tuning
        "new_vaccines": 1, # nye vaksiner som kommer i sirkulasjon hver rund
        "new_patients": 1, # mengde folk i kritisk kondisjon som kan behandles per rund 
        "m": 0.03, # movment magnitude
        "cd": 0.02, # radius for collision detection

        "cdsq": 0.02 ** 2 # 0.02 er verdien i "cd"


    }


