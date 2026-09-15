#!/usr/bin/env bash
# Pensado para correr dentro de WSL2 (Ubuntu). stable-retro no publica wheels
# para Windows nativo, solo Linux y macOS, por eso el proyecto se trabaja
# desde una distro Linux dentro de WSL2 en vez de PowerShell/cmd.
set -e

echo "=== xmen-rl-project setup ==="

if [ ! -d "venv" ]; then
    echo "Creando entorno virtual en venv/..."
    python3 -m venv venv
else
    echo "El entorno virtual venv/ ya existe, se omite la creacion."
fi

echo "Activando entorno virtual..."
source venv/bin/activate

echo "Actualizando pip..."
pip install --upgrade pip

echo "Instalando dependencias de requirements.txt..."
pip install -r requirements.txt

echo
echo "=== Setup terminado ==="
echo "Para seguir trabajando, corre: source activate.sh"
echo "Luego prueba el entorno con: python src/test_env.py"
echo
