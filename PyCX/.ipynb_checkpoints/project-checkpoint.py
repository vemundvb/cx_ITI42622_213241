
import pycxsimulator
from pylab import *
import copy as cp
import uuid
import random


# mutation rate when smitting:
# when deseas smitts others, it has a chance to mutate. 
# if deseas mutates, new vaccines for it will have to be produced
# and people that are immune to some previous version of it, are not immune this this deseas
smut = 0.01
mutations = [] # list of mutations
new_vaccines_every_turn = 0

# healthy
ns = 5 # initial sick population
m = 0.03 # movment magnitude
c = 'ro' # color of sick
sick_t = 50 # turns sickness lasts

 


cd = 0.02 # radius for collision detection
cdsq = cd ** 2








# risikogrupper
# folk har en sannsynlighet for å være i en risikogruppe, for å simulere forskjellige befolkninger
"""
n: initial population
ps: probability of sickness
pd: probability of death when smitten
c: color - når man blir syk blir det en mørkere shade av farga
"""
grupper = {
    # risikogrupper
    "alder_80": {"n": 1, "ps": 0.2, "pd": 0.3, 'c': 'ro},
    "alder65_79": {"n": 1, "ps": 0.2, "pd": 0.3},
    "kreft": {"n": 1, "ps": 0.2, "pd": 0.3, 'c'},
    "diabetes": {"n": 1, "ps": 0.2, "pd": 0.3},
    "fedme": {"n": 1, "ps": 0.2, "pd": 0.3},
    "nyresvikt": {"n": 1, "ps": 0.2, "pd": 0.3},
    "funksjonsnedsettelse": {"n": 1, "ps": 0.2, "pd": 0.3},
    "demens": {"n": 1, "ps": 0.2, "pd": 0.3},
    "psykisk_lidelse": {"n": 0.1, "ps": 0.2, "pd": 0.3},
    "downs": {"n": 1, "ps": 0.2, "pd": 0.3},
    
    "ingen_risiko": {"n": 0.1, "ps": 0.2, "pd": 0.3}    
}
sum_n = lambda g: sum(v["n"] for v in g.values())
n = sum_n(grupper)


    
# statistics
def create_mutation():
    return {
        "unid" = uuid.uuid4()
        
        "deaths" = 0
        "critical_condition" = 0
        "total_infected" = 0
        "total_vaccinated" = 0
        "total_recovered" = 0
        "total_suceptible" = 0 # eks ikke vaksinert, i nærheten syke, risikogruppe
        
        "symptometic" = 0 # hva er det?
        "asyomptometic" = 0 #hva er det?
    }

def add_mutation(current_mutations):
    return current_mutations + [ create_mutation() ]

# legger til første sykdomsvariasjon, før simulasjon starter
mutations = add_mutation(mutations)


class agent:
    def __init__(smitten_by, x, y, gruppe, symptotic):
        # agent will become immune to a deseas if:
        # it is smitten by the deseas
        # it is vaccinated against it
        self.immunities = [] # list of mutations agent in immune to, each holds unid
        self.smitten_by = smitten_by # none if not smitten, otherwise an unid
        self.x = x # int, posisjon
        self.y = y # int, posision
        self.gruppe = gruppe # risikogruppe
        self.vaccinated_for = [] # sykdommer som har vaksinert for, unid for mutasjonen
        self.m = 0.3 # movment magnitude
        self.sick_t = 0 # turns been sick
        self.symptotic = symptotic # jeg tror det er en periode før man blir kjenner at man er syk, der man bare har symptomer

        

def initialize():
    global agents
    agents = []
    for key in gruppe:
        for i in item["n"]:
            deseas_p = random.random()
            deseas = mutations[0]["unid"] if ideseas_p > ( ns/(n+ns) ) else None
            if deseas != None:
                mutations[0]["total_infected"] += 1
            ag = agent(
                smitten_by=deseas,
                x=random(),
                y=random(),
                gruppe=key,
                symptotic=True if deseas != None else False
            )
            

def observe():
    global agents
    cla()
    
    sicks = [ag for ag in agents if ag.smitten_by != None]
    if len(sicks) > 0:
        x = [ag.x for ag in sick]
        y = [ag.y for ag in sick]
        plot(x, y, c)
        
    healthies = [ag for ag in agents if ag.smitten_by == None]
    for key in grupper:
        x = [ag.x for ag in healthies if ag.gruppe == key]
        y = [ag.y for ag in healthies if ag.gruppe == key]
        plot(x, y, grupper[key]['c'])
        
    axis('image')
    axis([0, 1, 0, 1])




    
def update_one_agent():
    global agents
    if agents == []:
        return

    ag = choice(agents)

    # simulating random movement... TODO: isolerer hvis syk (og vet er syk)
    m = ag.m ###
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # sykdom går potensielt over
    # dør potensielt av sykdom
    # tar potensielt en vaksine for en mutasjon, som ikke har tatt vaksine for ... ?? burde man ta vaksine hvis man er syk?
    # blir potensielt smittet av en syk nabo, sykdommen blir potensielt en mutasjon



    
    # detecting collision and simulating death or birth
    neighbors = [nb for nb in agents if nb.type == 's' and ag.type == 'h' 
                 and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]

    if ag.type == 'h':
        if len(neighbors) > 0: # if there are foxes nearby
            if random() < ps and ag.immune == False:
                ag.type = 's' # cell gets smitten
    else:
        ag.sick_t += 1
        if ag.sick_t == sick_t:
            ag.type = 'h'
            ag.immune = True

    



    
    
def update():
    global agents
    t = 0.
    while t < 1. and len(agents) > 0:
        t += 1. / len(agents)
        update_one_agent()

pycxsimulator.GUI().start(func=[initialize, observe, update])




