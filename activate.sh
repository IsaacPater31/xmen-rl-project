#!/usr/bin/env bash
# Este script debe ejecutarse con "source", no directamente, para que la
# activacion del venv quede en tu shell actual:
#   source activate.sh

if [ ! -d "venv" ]; then
    echo "No se encontro venv/. Corre ./setup.sh primero."
    return 1 2>/dev/null || exit 1
fi

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "Este script debe ejecutarse con 'source', no directamente:"
    echo "  source activate.sh"
    exit 1
fi

source venv/bin/activate
echo "Entorno virtual activado. Ya podes correr: python src/test_env.py"
