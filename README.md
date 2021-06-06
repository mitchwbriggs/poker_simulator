# Poker Simulator

# Overview
Generate win probability estimates for specific Texas Hold'em scenarios. The GUI takes in your cards, the cards on the board, and the number of opponents remaining in the hand as inputs. Monte Carlo simulations are run on the backend and the resultant win percentage is returned as an output. The estimate typically falls within +/- 1 percentage point of the actual win probability value.

Please note that the project is a work-in-progress! The GUI is still quite crude and does not feature any error handling. Simulation performance also has substantial room for improvement. That said, the program is more than sufficient for it's most likely use case: generating a quick-and-dirty hand equity estimate. Enjoy! (: 

## File Descriptions
main.py
  - Main project file; run to launch GUI

my.kv
  - GUI formatting and styling; written in KV (Kivy language)

holdem_engine.py
  - Classes and functions related to general Texas Hold'em mechanics (Card and Deck objects, naive hand evaluation, etc.)

simulation_engine.py
  - Classes and functions related to setting up and running poker simulations

hash_tools.py
  - Classes and functions related to the creation of a hash lookup table that can be used to evaluate poker hands

hash_lookup.pickle
  - 'Pickle' file that contains hand evaluation lookup table; used instead of a CSV to reduce memory load

test.py
  - Used to test holdem_engine.py


## Dependencies
- Python
  - Pandas
  - NumPy
  - Pickle
  - Kivy
  - Random
  - Functools
  - Itertools
  - Random
  - Collections
  - Threading
