"""
This module contains the logic for new movie recommendations.
It is supposed to run in the background.
"""

from time import sleep

sleep(30)

# Check that the recommendations directory exists or create it.
# Draws 3 random movies present in random collections.
# It can be the same film three times.
# Get 3 recommendations for these 3 films, they cannot be identical or already present in a collection.
# Download the posters of these 3 recommendations in the recommendations directory.
# Obtain and organize the trailer links in a json file.
