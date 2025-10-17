# Prompt for Claude CLI: Deploying the Motia Project

**Objective:** To deploy the `motia` project on a fresh Debian-based Linux server. You will act as a DevOps assistant, executing the necessary commands to install dependencies, clone the repository, and run the application.

---

### Phase 1: Install Prerequisites

1.  **Update package lists:**
    ```bash
    sudo apt update
    ```
2.  **Install Git:**
    ```bash
    sudo apt install -y git
    ```
3.  **Install Docker and Docker Compose:**
    ```bash
    # Install Docker
    sudo apt install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker

    # Install Docker Compose
    sudo apt install -y docker-compose
    ```
4.  **Add current user to the `docker` group to run Docker without `sudo`:**
    ```bash
    sudo usermod -aG docker ${USER}
    echo "Please log out and log back in for the group changes to take effect."
    ```

---

### Phase 2: Clone and Configure the Project

1.  **Clone the repository using SSH:**
    ```bash
    git clone git@github.com:maxfraieho/motia_drn_start.git motia
    cd motia
    ```
2.  **Populate the `drakonwidget.js` file:**
    This file is required for the DRAKON viewer. Download its content from the official repository.
    ```bash
    curl -o tools/drakon-viewer/public/js/drakonwidget.js https://raw.githubusercontent.com/stepan-mitkin/drakonwidget/main/js/drakonwidget.js
    ```
3.  **Generate the initial diagram index:**
    This command analyzes an existing step and creates the necessary index for the viewer.
    ```bash
    ./unified-motia-workflow.sh drakon bot-service
    ```

---

### Phase 3: Launch and Access the Application

This section also serves as the **official instruction for launching the DRAKON diagram viewer**.

1.  **Start the DRAKON viewer service:**
    This command uses Docker Compose to launch a local Nginx server that serves the diagrams.
    ```bash
    ./unified-motia-workflow.sh view
    ```
2.  **Access the viewer:**
    Open a web browser and navigate to the following address:
    [http://localhost:8080](http://localhost:8080)

    The list of diagrams will be updated automatically every time you run the `./unified-motia-workflow.sh drakon` or `./unified-motia-workflow.sh full-pipeline` commands.
