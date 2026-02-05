FROM mcr.microsoft.com/vscode/devcontainers/python:3.14

RUN rm -f /etc/apt/sources.list.d/yarn.list
RUN apt update && apt install --yes wget bash-completion make

COPY Makefile /opt/Makefile
RUN cd /opt && make install

USER vscode
RUN poetry completions bash >> ~/.bash_completion

ENV PATH="$PATH:/workspaces/i13c-lang/scripts"
