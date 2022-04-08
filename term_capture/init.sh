source ~/.bashrc

PS1='\[\e[32m\]❯\[\e[m\] \[\e[94m\]/home/project\[\e[m\] \[\e[32m\]❯\[\e[m\] '
PROMPT_COMMAND='export PROMPT_COMMAND=:; trap '"'"'printf "\n"'"'"' DEBUG;'

