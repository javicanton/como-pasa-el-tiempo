# Mejora de Imágenes

Script en Python para mejorar la calidad de imágenes mediante upscaling y autoenhance.

## Características

- Upscaling de imágenes (aumento de resolución)
- Mejora automática de imágenes (contraste, brillo, saturación y nitidez)
- Procesamiento por lotes de imágenes
- Interfaz interactiva para elegir las mejoras deseadas

## Requisitos

- Python 3.x
- OpenCV (cv2)
- Pillow (PIL)

## Instalación

1. Clona este repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
```

2. Instala las dependencias:
```bash
pip install opencv-python Pillow
```

## Uso

1. Ejecuta el script:
```bash
python enhancer.py
```

2. Sigue las instrucciones en pantalla:
   - Introduce la ruta de la carpeta con las imágenes
   - Elige si quieres hacer upscale (y/n)
   - Elige si quieres aplicar autoenhance (y/n)

3. Las imágenes mejoradas se guardarán en la carpeta "Output"

## Opciones de Mejora

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
├── enhancer.py         # Script principal
├── Output/             # Carpeta para imágenes procesadas
└── README.md          # Este archivo
```

## Notas

- Las imágenes originales no se modifican
- Se procesan archivos .jpg, .jpeg y .png
- Se pueden aplicar ambas mejoras o solo una
- Las imágenes mejoradas se guardan en la carpeta "Output"

---

**¡Cualquier sugerencia o mejora es bienvenida!**
