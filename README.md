# Proyecto de Procesamiento y Presentación de Imágenes

Este proyecto contiene un conjunto de aplicaciones para trabajar con imágenes, permitiendo crear presentaciones, mejorar la calidad de las fotos y crear collages comparativos.

## Aplicaciones Incluidas

### 1. Animación de Fotos (`animacion.py`)

Crea una presentación profesional con tus fotos, incluyendo transiciones suaves y efectos visuales.

### 2. Mejora de Imágenes (`enhancer.py`)

Herramienta para mejorar la calidad de tus imágenes mediante upscaling y ajustes automáticos de color y nitidez.

### 3. Collage Comparativo (`collage.py`)

Crea collages que muestran fotos de "antes y después", perfecto para mostrar mejoras, transformaciones o cambios a lo largo del tiempo.

## Requisitos

- Python 3.x
- Pillow (PIL)
- MoviePy (para animacion.py)
- OpenCV (cv2) (para animacion.py y enhancer.py)

## Instalación

```bash
pip install Pillow moviepy opencv-python
```

## Uso

### Animación de Fotos (`animacion.py`)

1. Coloca las fotos que deseas incluir en la presentación en una carpeta
2. Asegúrate de tener el archivo de música de fondo en el directorio raíz
3. Ejecuta el script:

```bash
python animacion.py
```

4. Sigue las instrucciones en pantalla para personalizar tu presentación
5. El video resultante se guardará en la carpeta `Output`

### Mejora de Imágenes (`enhancer.py`)

1. Ejecuta el script:

```bash
python enhancer.py
```

2. Sigue las instrucciones en pantalla:
   - Introduce la ruta de la carpeta con las imágenes
   - Elige si quieres hacer upscale (y/n)
   - Elige si quieres aplicar autoenhance (y/n)
3. Las imágenes mejoradas se guardarán en la carpeta "Output"

### Collage Comparativo (`collage.py`)

1. Ejecuta el script:

```bash
python collage.py
```

2. Sigue las instrucciones en pantalla:
   - Selecciona las fotos de "antes"
   - Selecciona las fotos de "después"
   - Elige el estilo de collage
   - Personaliza el diseño y los efectos

## Características de Mejora de Imágenes

### Upscale

- Aumenta la resolución de las imágenes al doble
- Usa interpolación bicúbica para mantener la calidad

### Autoenhance

- Mejora el contraste (+20%)
- Ajusta el brillo (+10%)
- Aumenta la saturación (+10%)
- Mejora la nitidez (+20%)

## Estructura del Proyecto

```
.
├── animacion.py        # Script para crear presentaciones con fotos
├── enhancer.py         # Script de mejora de imágenes
├── collage.py          # Script de creación de collages comparativos
├── Output/             # Carpeta para archivos procesados
└── README.md          # Este archivo
```

## Características Destacadas

- **Presentaciones Profesionales**: Crea presentaciones con transiciones suaves y efectos visuales
- **Mejora de Calidad**: Optimiza tus imágenes con ajustes automáticos
- **Collages Comparativos**: Muestra transformaciones y cambios de manera visual y atractiva
- **Interfaz Intuitiva**: Fácil de usar con instrucciones claras en pantalla
- **Personalización**: Ajusta los parámetros según tus necesidades

## Créditos

### Sonido del Obturador

El sonido del obturador de la cámara (`shutter.mp3`) es un efecto de sonido proporcionado por:

- Autor: [kakaist](https://pixabay.com/es/users/kakaist-48093450/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=314056)
- Fuente: [Pixabay](https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=314056)
- Enlace directo: [Camera Shutter Sound Effects](https://pixabay.com/es/sound-effects/search/camera-shutter/)

---

**¡Cualquier sugerencia o mejora es bienvenida!**
