import argparse
from typing import List, Dict, Optional, Tuple
import random
from datetime import datetime


def get_everything() -> Dict[str, Dict[str, List[str]]]:
    return eval(open("food_finder.options").read())


def get_categories(everything: Dict[str, Dict[str, List[str]]]) -> List[str]:
    categories = []
    for place in everything:
        categories += everything[place]["category"]

    return list(set(categories))


def parse_args() -> List[str]:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--craving", nargs="+", type=str,
                        dest='craving')

    return parser.parse_args().craving


def get_time() -> Tuple[int, int, int]:
    now = datetime.now()
    return now.weekday(), now.hour, now.minute


def is_open(everything: Dict[str, Dict[str, List[str]]],
            day_of_week: int,
            hour: int,
            minute: int) -> Dict[str, Dict[str, List[str]]]:
    currently_open = {}
    for place in everything:
        todays_hours = everything[place]["hours"][day_of_week]
        if todays_hours[0] <= hour < todays_hours[1]:
            currently_open[place] = everything[place]
    return currently_open


def pick(cravings: Optional[List[str]],
         everything: Dict[str, Dict[str, List[str]]]):
    day_of_week, hour, minute = get_time()
    possible = is_open(everything, day_of_week, hour, minute)
    if cravings is not None:
        def satasifies(place: str) -> bool:
            for category in everything[place]['category']:
                if category in cravings:
                    return True
            return False
        possible = filter(satasifies, everything)
    return random.choice(list(possible))


def main() -> None:
    cravings = parse_args()
    everything = get_everything()
    place = pick(cravings, everything)
    day_of_week, hour, minute = get_time()
    print("You should go to", place)
    print("  Hours:", everything[place]["hours"][day_of_week])
    print("  Address:", everything[place]["addr"])


if __name__ == '__main__':
    main()
