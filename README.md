# Poker Simulator

# Overview
Generate win probability estimates for specific Texas Hold'em scenarios. The GUI takes in your cards, the cards on the board, and the number of opponents remaining in the hand as inputs. Monte Carlo simulations are run on the backend and the resultant win percentage is returned as an output. This estimate typically falls within +/- 1 percentage point of the actual win probability value.

Please note that the project is a work-in-progress! The GUI is crude and simulation performance leaves something to be desired. That said, the program is sufficient for it's most likely use case: generating a quick-and-dirty hand equity estimate. Enjoy! (: 

## File Descriptions
main.py
  - GUI file; run to launch application

holdem_engine.py
  - Classes and functions related to general Texas Hold'em mechanics (Card and Deck objects, naive hand evaluation, etc.)

simulation_engine.py
  - Classes and functions related to setting up and running poker simulations

hash_tools.py
  - Classes and functions used to create a hash lookup table for efficient poker hand evaluation

hash_lookup.pickle
  - 'Pickle' file that contains hand evaluation lookup table; used instead of a CSV to reduce memory load

test.py
  - Used to test holdem_engine.py

app_icon.png
  - Image used for app icon


## Dependencies
- Python
  - Pandas
  - NumPy
  - Pickle
  - PyQt5
  - Random
  - Functools
  - Itertools
  - Collections
  - Threading
