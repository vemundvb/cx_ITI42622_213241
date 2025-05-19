



# class representing an agent
class agent:
    def __init__(self, sick, x, y, gruppe):
        self.x = x # int, posisjon
        self.y = y # int, posision
        self.gruppe = gruppe #
        self.sick = sick
        self.symptometic_t = 0 # turns been sick
        self.critical_t = 0 #  turns critical
        self.dead = False
        self.immune = sick
        self.critical = False












