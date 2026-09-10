#!/bin/bash

# Verificar si se pasó un archivo como argumento
if [ -z "$1" ]; then
    echo "Error: Debes proporcionar un archivo."
    echo "Uso: $0 archivo.Rmd o $0 archivo.ipynb"
    exit 1
fi

ARCHIVO="$1"
NOMBRE="${ARCHIVO%.*}"
EXTENSION="${ARCHIVO##*.}"

# Validar que el archivo exista
if [ ! -f "$ARCHIVO" ]; then
    echo "Error: El archivo '$ARCHIVO' no existe."
    exit 1
fi

# Conversión según la extensión
case "$EXTENSION" in
    rmd|Rmd)
        echo "Detectado archivo Rmd. Convirtiendo a ipynb..."
        jupytext --to notebook "$ARCHIVO"
        ;;
    ipynb)
        echo "Detectado archivo ipynb. Convirtiendo a Rmd..."
        Rscript -e "rmarkdown::convert_ipynb('$ARCHIVO', '${NOMBRE}_ipynb.Rmd')"
        ;;
    *)
        echo "Error: Extensión '.$EXTENSION' no soportada."
        echo "Solo se admiten archivos .Rmd o .ipynb"
        exit 1
        ;;
esac

echo "¡Conversión finalizada con éxito!"

