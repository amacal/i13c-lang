FROM mcr.microsoft.com/vscode/devcontainers/python:3.14

RUN apt update && apt install --yes wget graphviz bash-completion
RUN pipx install poetry==2.2.1

USER vscode
RUN poetry completions bash >> ~/.bash_completion
