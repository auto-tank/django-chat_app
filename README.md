# Project Setup

Basic chat app with the OpenAI Langchain API using Django for the Python backend.

## Instructions

### Prerequisites

Before starting, ensure you have the following installed:

- Python 3.10 or higher
- Git

### Steps

1. **Clone the repository**

   This step downloads the project files to your local machine.

   ```bash
   git clone https://github.com/drigohhh/django-chat_app
   cd django-chat_app
   ```

2. **Copy the `settings.dev.py` into a local folder**

   Create a local directory and copy the settings file needed for development.

   ```bash
   # Windows
   mkdir local
   copy .\core\project\settings\templates\settings.dev.py .\local\settings.dev.py
   ```

   ```bash
   # Linux
   mkdir local
   cp ./core/project/settings/templates/settings.dev.py ./local/settings.dev.py
   ```

   If this doesn't work, create the folder 'local' at the top of your environment and copy the file manually.

3. **Install [Poetry](https://python-poetry.org/)**

   Poetry will manage your dependencies and create a virtual environment.

   ```bash
   python -m pip install poetry
   ```

   Make sure to activate the virtual environment in your IDE.

4. **Set your API key in the environment variable**

   In `.local/settings.dev.py`, configure your OpenAI API key for the application.

   ```python
   os.environ["OPENAI_API_KEY"] = ""  # type: ignore  # noqa: F821
   ```

   This variable should be set in the environment created by Poetry. **Ensure** that your code runs from that environment.

5. **Run the Makefile command**

   This command will install the dependencies and automatically migrate the database.

   ```bash
   make update
   ```

6. **Host the server**

   Start your Django server to run the application.

   ```bash
   make runserver
   ```

## Known Bugs

- **Python 3.13 seems to break the installation of some dependencies.**
