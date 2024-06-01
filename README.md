# ResumeAI

This project generates a resume in PDF format using a combination of data from a JSON file and an HTML template.

## Prerequisites

Ensure you have the following software installed:

- Docker
- Python 3.x
- pip

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/nirtuttnauer/resumeai.git
    cd resumeai
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Create a `.env` file in the root directory of the project and add your OpenAI API key:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key_here
    ```

2. Ensure you have the `mydata.json` file in the root directory with your resume data.

## Development Container Setup

This project includes a development container for a consistent development environment using Visual Studio Code's Dev Containers extension. Follow the steps below to set it up:

1. **Install Docker**:

   - Windows / macOS: Install Docker Desktop.
   - Linux: Follow the official install instructions for Docker CE/EE for your distribution.

2. **Install Visual Studio Code**:

   - Download and install [Visual Studio Code](https://code.visualstudio.com/).

3. **Install the Dev Containers extension**:

   - Open Visual Studio Code.
   - Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or by pressing `Ctrl+Shift+X`.
   - Search for `Dev Containers` and click `Install`.

4. **Open the project in the development container**:

   - Open the project folder in Visual Studio Code.
   - Press `F1` to open the Command Palette, type `Dev Containers: Reopen in Container`, and select it.

5. **Build and run the development container**:

   - Visual Studio Code will automatically build the development container based on the configuration in the `.devcontainer` folder and reopen the project within the container.

## Usage

To generate the resume, run the `main.py` script:

```sh
python main.py
```

This will create a resume.pdf file in the root directory.

## Project Structure

resumeai/
├── main.py
├── mydata.json
├── requirements.txt
├── resume_template.html
├── .env
└── .devcontainer/
    └── devcontainer.json
