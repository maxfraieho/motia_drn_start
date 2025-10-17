# Initial Command for Claude CLI to Deploy the Motia Project

Here is the single, self-contained command to provide to the Claude CLI. This command initiates the full deployment of the `motia` project on a new server by instructing the AI to clone the repository and then follow the detailed instructions within it.

## The Command

Copy and paste the following command into your terminal on the new server where Claude CLI is installed:

```bash
claude "Hello. Please deploy the 'motia' project for me on this fresh Debian-based server. Here are your instructions: First, clone the project repository by running 'git clone git@github.com:maxfraieho/motia_drn_start.git motia'. After cloning, change into the 'motia' directory. Inside, you will find a file named 'claude-deployment-prompt.md'. Please read that file carefully and execute all the shell commands listed within it, in order, to complete the setup and deployment. Let me know if you encounter any issues."
```

## How to Use

1.  SSH into your new, empty server.
2.  Ensure the Claude CLI tool is installed and configured.
3.  Ensure that SSH keys are configured on the server to allow cloning from your private GitHub repository.
4.  Execute the command above.

Claude will then perform all the necessary steps to get the project and the DRAKON viewer running.
