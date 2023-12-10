# Pymoman
A lightweight movie manager using Python and PySide6.

## Introduction
PyMoman, which simply stands for Python Movie Manager, is a movie management tool that offers a variety of features.
It allows you to start organizing your movie collection by creating different collections and adding the films you prefer.
You don't even need to worry about API keys or accounts on external websites, as the application takes care of fetching movie information from the internet automatically.
While there's still work to be done to refine the code and add more features, PyMoman already provides you with a straightforward way to create movie collections.

## Screenshots

![01](https://github.com/Tony-TRT/Pymoman/assets/146631446/0830454c-3313-46eb-9295-a89b3422633d)


![02](https://github.com/Tony-TRT/Pymoman/assets/146631446/bb31e0c1-217d-4eb2-ae45-d3eadb484780)

## How to install
It works on Windows and Linux (tested on Debian Sid), although there are some display faults in QComboBoxes under Linux.
I recommend using Python 3.11 because that's the version I work with.

Please keep in mind that this is an ongoing project, and many features still need to be perfected.

1) Clone the repository:
   
   `git clone https://github.com/Tony-TRT/Pymoman.git`

2) Create a virtual environment and install the dependencies:
   
   `cd Pymoman`
   
   `python -m venv env`

   `source env/Scripts/activate`

   `pip install -r requirements.txt`

3) Make sure to use the virtual environment and run 'run.py'.

## How to use
You must first create a collection, open it, and then add movies.
In order to retrieve information from the internet, the application requires the release date of the movie, as we can all agree that 'Planet of the Apes' from 1968 is not the same film as 'Planet of the Apes' from 2001 :).
Please note that regardless of the actions you take, everything will be lost upon closure if you do not save!

## How to help
Any help is welcome; there are no strict constraints as long as the coding style remains somewhat consistent.
I'm not an expert myself, and it's quite possible that some parts of my program are poorly optimized, so I would even be very grateful for assistance !
