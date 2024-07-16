# Biblioteca Midossi📚 - Backend
Backend API for [Midossi](https://www.midossi.edu.it/)'s digital library.
## Installation
### Install Python
Download Python 3.10+ from the [official site](https://python.org)

> [!Note] 
> This project was developed using Python 3.10.2 and newer versions, and might not work with older versions

### Clone this repository
To clone the repository, use one of the following commands depending on whether the repository is public or private:

#### Public Repositiory:
```bash
git clone https://github.com/Biblioteca-Midossi/BibliotecaBackend.git
```
#### Private Repository:
Use [GitHub Desktop](https://desktop.github.com/) or:
```bash 
git clone git@github.com:Biblioteca-Midossi/BibliotecaFrontend.git
```
> [!Note]
> Authentication with SSH is required for private repositories.

### Install dependencies
It is recommended to create a [Python virtual environment](https://docs.python.org/3/library/venv.html):
```bash
python3 -m venv .venv
```

Activate the virtual environment and install the dependencies:
```bash 
# On Windows
.venv\Scripts\activate

# On Unix or Unix-like systems
source .venv/bin/activate

# Install dependencies (may not finish on windows because of hypercorn)
pip install -r requirements.txt
```


### Other requirements
- A PostgreSQL database
- A Redis database

### Configure the environment
Rename `.env_template` to `.env` and fill in the appropriate credentials.

### Running the server
On Unix-like systems (Linux, MacOS):
```bash
source start.sh [-<process manager abbreviation> | --<process manager>]
```
> Check `source start.sh --help` for all the available process managers

On Windows:
```bash
uvicorn App:app --host 0.0.0.0 --port 8000
```

> [!Note] 
> It is recommended to run the system on Unix-like systems for stability and for more control over it. 
> In both cases, the API will listen to every IPv4 address available to the host on port 8000. To change that,
> you can use a specific IPv4 address instead of 0.0.0.0. You can also change the port it listens to, 
> but remember to also change it on the frontend, if you're using it.