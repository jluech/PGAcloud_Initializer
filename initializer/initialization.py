import logging
import random

from population.individual import Individual
from utilities import utils


def apply_initialization(amount):
    # Initializes and returns a list of <amount> randomly generated Individual's.
    logging.info("Initializing {amount_} individuals.".format(amount_=amount))
    capacity = int(utils.get_property("item_count"))

    generated_individuals = []
    for i in range(amount):
        solution = ""
        for c in range(capacity):
            bit_flip = random.randint(0, 99)
            solution += "1" if (bit_flip % 2) else "0"
        generated = Individual(solution)
        generated_individuals.append(generated)
        logging.info("Generated {idx_} - {sol_}".format(
            idx_=i+1,
            sol_=generated)
        )

    return generated_individuals
