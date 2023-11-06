# Pymoman
A lightweight movie manager using Python and PySide6.

## Introduction
PyMoman, which simply stands for Python Movie Manager, is a movie management tool that offers a variety of features.
It allows you to start organizing your movie collection by creating different collections and adding the films you prefer.
You don't even need to worry about API keys or accounts on external websites, as the application takes care of fetching movie information from the internet automatically.
While there's still work to be done to refine the code and add more features, PyMoman already provides you with a straightforward way to create movie collections.

## Screenshots

![01](https://github.com/Tony-TRT/Pymoman/assets/146631446/2f27452e-b9a5-4ed7-933a-36a78f11c6f2)


![02](https://github.com/Tony-TRT/Pymoman/assets/146631446/c58bd31c-1aaa-4136-bb90-c43219014558)


![03](https://github.com/Tony-TRT/Pymoman/assets/146631446/3e3de780-e653-4037-8178-49dd1503d2a1)


![04](https://github.com/Tony-TRT/Pymoman/assets/146631446/4bef1ee2-2f07-4650-b01a-d8c672060715)

## How to install
It works on Windows and Linux (tested on Debian Sid), although there are some minor display issues on Linux.
I recommend using Python 3.11 because that's the version I work with.

It does not work with Python 3.12 (strange display glitches) and has not been tested with other versions.

Please keep in mind that this is an ongoing project, and many features are yet to be implemented.

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
