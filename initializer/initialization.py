import logging

from population.individual import Individual


def apply_initialization(amount):
    # Initializes and returns <amount> new Individual's.
    logging.info("Initializing {amount_} individuals.".format(amount_=amount))

    return [Individual("110010")]
