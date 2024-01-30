from character import Character

"""
    The class `Brain` represents the "brains" (or artificial intelligence, AI) of
    virtual characters that inhabit two dimensional grid worlds. A brain is equipped
    with an algorithm for determining what a character should do during its turn in a disease
    simulation. 
    
    Concrete class that extend this class need to provide implementations for the abstract
    `move_body` method; each such concrete class can represent a new kind of moving behavior.

    The given parameter body is the character that the brain controls.
"""


class Brain(Character):

    def __init__(self, body):
        self.body = body

    def move_body(self):
        pass

    # def is_susceptible(self):
    #    pass

    def is_infected(self):
        pass

    # def is_recovered(self):
    #    pass
