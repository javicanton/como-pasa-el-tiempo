# ¡Cómo pasa el tiempo!

Un script para crear collages comparativos de imágenes de antes y después. Ideal para ver la evolución de cualquier cosa: personas, objetos, proyectos, mascotas, plantas... ¡y sorprenderte con el paso del tiempo!

# Collage Fotos

Este script está pensado para que puedas crear collages comparativos de imágenes, es decir, juntar el "antes" y el "después" en una sola imagen de forma automática y elegante. Ideal para comparar cualquier cosa: personas, objetos, proyectos, etc.

## ¿Qué hace este script?
- Lee una lista desde un archivo CSV (con columnas: ID, Nombre, Apellido 1, Apellido 2 opcional).
- Busca dos fotos por cada entrada (antes y después) en la carpeta `Fotos`.
- Genera un collage para cada caso, colocando ambas fotos lado a lado, ajustando el alto al canvas (1920x1080 px).
- Añade el nombre completo en la parte inferior, en un recuadro blanco con borde azul y esquinas redondeadas.
- Guarda los collages en la carpeta `Output`.

## Requisitos
- Python 3.7 o superior
- Paquetes: `pandas`, `Pillow`
- Una fuente TrueType instalada (por ejemplo, Arial)

Puedes instalar los requisitos con:
```bash
pip install pandas pillow
```

## Estructura de carpetas
```
.
├── Fotos/                # Aquí van las fotos (formato: ID_bf.jpg/png y ID_af.jpg/png)
├── Output/               # Aquí se guardan los collages generados
├── Lista.csv             # Lista de casos (se ignora en el repositorio)
├── collage photos.py     # Script principal
```

## Formato del CSV
El archivo debe tener al menos las siguientes columnas:
- `ID` (identificador, por ejemplo: 001, 002...)
- `Nombre`
- `Apellido 1`
- `Apellido 2` (opcional)

## Ejecución
Coloca las fotos y el CSV en las carpetas indicadas y ejecuta:
```bash
python collage photos.py
```

Los collages se guardarán en la carpeta `Output`.

---

**¡Cualquier sugerencia o mejora es bienvenida!** 