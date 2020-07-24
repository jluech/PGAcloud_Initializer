import logging
import random

from population.individual import Individual
from utilities.utils import get_property


def apply_initialization(amount):
    # Initializes and returns a list of <amount> randomly generated Individual's.
    logging.info("Initializing {amount_} individuals.".format(amount_=amount))
    capacity = get_property("knapsack_capacity")

    generated_individuals = []
    for i in range(amount):
        solution = ""
        for c in range(capacity):
            bit_flip = random.randint(0, 99)
            solution += "1" if (bit_flip % 2) else "0"
        generated_individuals.append(Individual(solution))
        logging.debug(solution)  # TODO: remove

    return generated_individuals