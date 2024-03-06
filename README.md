# Biblioteca Midossi📚 - Backend
## Installation
### Install Python
> Download Python 3.10+ from the [official site](https://python.org) \

> Note: this project was developed using Python 3.10.2, and might not work on older version

### Clone this repository
> You can use \
> `git clone https://github.com/Biblioteca-Midossi/BibliotecaBackend.git` \
> **If the repository is public.**

> **You must use** \
> [GitHub Desktop](https://desktop.github.com/) \
> or \
> `git clone git@github.com:Biblioteca-Midossi/BibliotecaFrontend.git` (Must be authenticated with SSH) \
> **If the repository is private.**

### Install dependencies
> It is recommended to create a python virtual environment \
> You can do so by running `python -m venv .venv` in the root folder

> After activating the venv you can use `pip install -r requirements.txt` to install all the dependencies

### Running the server
> You must have uvicorn installed to do this, but you should already have it if you followed the step above
> Run `uvicorn App:app --host 0.0.0.0 --port 8000` to run the server on your network, on the port 8000.

> Note: you can change the host ip and the port, but it is not advices to do so if you're using this with the frontend,
> as they're made to work with this port and you would also need to change some things there