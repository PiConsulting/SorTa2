import os
import json
import random
import argparse
import logging


def pretty_print(*args):
    print('\n')
    print("*"*60)
    print(*args, sep='')
    print("*" * 60)


def load_json_data(jsonpath):
    with open(jsonpath, 'r') as file:
        return json.load(file)


def save_data(data, jsonpath):
    with open(jsonpath, 'w') as file:
        json.dump(data, file, indent=4)


def lottery(participants):
    win = None
    while True:
        win = random.choices(participants, weights=probs)
        if win[0] != last_host:
            break
    return win[0]


CUR_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Realiza un sorteo de los participantes.')
    parser.add_argument("-a", "--add", type=str, default="", metavar="\"Nombre Apellido\"",
                        help="Agregar un participante")
    parser.add_argument("-d", "--drop", type=str, default="", metavar="\"Nombre Apellido\"",
                        help="Borrar un participante")
    parser.add_argument("--version", action='version', version="0.06.2021.CristianC",
                        default=False, help="show version and exit")
    opt = parser.parse_args()

    logger = logging.getLogger('SorTa2')

    # Load participants
    data = load_json_data(os.path.join(CUR_DIR, "data", "sorteo.json"))

    last_host = data.get('Last_host', "")
    times_being_host = data.get('Times_being_host', {})

    if not(last_host and times_being_host):
        logger.warning("There aren't participants")

    # Add / drop participants
    if opt.add:
        times_being_host[opt.add] = 0
    if opt.drop and times_being_host.get(opt.drop, False):
        del times_being_host[opt.drop]

    names = list(times_being_host.keys())
    times = list(times_being_host.values())
    probs = list(map(lambda x: 1 if int(min(times)-x) == 0 else 0,
                     times))

    #pretty_print('Participantes: \n\t', '\n\t'.join(names))

    # Perform lottery
    winner = lottery(names)

    # #---------------------
    # #Shuffle the rest of participants, and add the host at the beginning
    # #---------------------
    names.remove(winner)
    random.shuffle(names)
    names.insert(0, winner)

    # Save and show results
    data['Last_host'] = winner
    data['Times_being_host'][winner] += 1

    pretty_print(f'Ganador: "{winner}"')

    pretty_print('Order: \n\t', '\n\t'.join(names))

    save_data(data, os.path.join(CUR_DIR, "data", "sorteo.json"))
    exit(0)