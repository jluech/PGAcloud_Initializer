import logging
import random

from population.individual import Individual
from utilities import utils


def apply_initialization(amount, individual_id):
    # Initializes and returns a list of <amount> randomly generated Individual's.
    capacity = int(utils.get_property("item_count"))

    generated_individuals = []
    if amount > 1:
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
    else:
        solution = ""
        for c in range(capacity):
            bit_flip = random.randint(0, 99)
            solution += "1" if (bit_flip % 2) else "0"
        generated = Individual(solution)
        generated_individuals.append(generated)
        logging.info("Generated {idx_} - {sol_}".format(
            idx_=individual_id+1,
            sol_=generated)
        )

    return generated_individuals
