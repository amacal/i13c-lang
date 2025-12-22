FROM mcr.microsoft.com/vscode/devcontainers/python:3.14

RUN apt update && apt install --yes wget graphviz bash-completion nasm
RUN pipx install poetry==2.2.1

USER vscode
RUN poetry completions bash >> ~/.bash_completion

ENV PYTHONPATH="/workspaces/i13c-lang/src"
ENV PATH="$PATH:/workspaces/i13c-lang/scripts"
