
import uuid

# ?? ok... at sykdommen har stor effekt. hvordan skal dette håndteres?
# man har en sannsynlighet for å dø...
# hva med at det heller er sannsynlighet for å komme i critical condition
# eks med covid så kan for noen sykdommen veldig skade halsen og lungene.
# man kan si man heller kommer i kritisk kondisjon, så har man en tid der man må behandles før man dør
# så i tillegg til nye vaksiner per runde, er det også kun så mange som kan behandles på sykehus
# de som har størst sannsynlighet for å komme i kritisk kondisjon, behandles først
# parametere:
# mengde folk som kan behandles på sykehus per runde
# sannsynlighet for å komme i kritisk kondisjon hvis smittet
# kan ta for nå mengde runder før man dauer? muligens etterhvert endre det til en sannsynlighet..


def add_step(step: int, stats):
    stats[f"step_{step}"] = {
        "deaths": 0,
        "critical": 0,
        "vaccinated": 0,
        "hospitelized": 0,
        "recovered": 0,
        # "total_suceptible": 0, ..bare ta antall som ikke er immun    
        "symptometic": 0  # hva er det?
        # total_asymptometic: ..bare ta antall som ikke er symptometic   
    }
    return stats



def init_stats():
    stats = {}
    stats["sum_deaths"] = 0
    stats["sum_critical"] = 0
    stats["sum_vaccinated"] = 0
    stats["sum_symptometic"] = 0
    stats["sum_hospitelized"] = 0
    stats["sum_recovered"] = 0
    stats = add_step(0, stats)
    return stats

    

