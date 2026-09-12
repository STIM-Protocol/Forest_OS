#!/bin/bash
# Forest OS: forest-r-engine container entrypoint
# Governance: Doc-414 Compliant (Zero em dashes, strict claims discipline)

set -e

# Handle web mode (RStudio Server)
if [ "$1" = "rstudio" ] || [ "$1" = "--web" ] || [ "$1" = "serve" ]; then
    echo "======================================================================"
    echo " Starting Forest OS RStudio Server"
    echo " Endpoint: http://localhost:8787"
    echo " Default user: rstudio"
    echo "======================================================================"
    exec /init
fi

# Handle evaluate flag
if [ "$1" = "-e" ] || [ "$1" = "--eval" ]; then
    shift
    exec Rscript -e "$@"
fi

# Default interactive R session if no command provided
if [ $# -eq 0 ]; then
    exec R --no-save --quiet
fi

# If argument ends with .R or .r, run with Rscript
if [[ "$1" == *.R ]] || [[ "$1" == *.r ]]; then
    exec Rscript "$@"
fi

# Fall through to execute custom command (e.g. bash, Rscript, etc.)
exec "$@"
