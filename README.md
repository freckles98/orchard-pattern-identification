#orchard-pattern-identification

This algorithm attempts to solve the problem of identifying planting patterns within ariel images of orchards.

## The Algorithm
The algorithm is based on the Hausdorff distance formula. It uses generated shapes as the base pattern to match against the orchard images, which are abstracted to geojson files.

## Libraries used
Each library was installed using `pip install`:
* shapely
* numpy
* sklearn
* pyplot
* scipy
* descartes
* json

## How to run the experiment
To run the experiment use the command `python3 main.py`

The prompt `Please orchard enter number: ` will appear. Choose your preferred orchard number from the numbers supplied in the `data` folder.

The next prompt `Please enter window size:` will appear. Please provide an int.

Then the experiment will commence.

## Acknowledgement
I would like to thank my supervisor Patrick Marais for the guidance provided during this project.