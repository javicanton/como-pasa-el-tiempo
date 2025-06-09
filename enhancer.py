import os
import cv2
from PIL import Image, ImageEnhance

# Aumentar el límite de tamaño de imagen de PIL
Image.MAX_IMAGE_PIXELS = None

def mejorar_imagen_autoenhance(ruta_entrada, ruta_salida):
    # Abrir imagen con PIL
    img = Image.open(ruta_entrada)
    
    # Mejorar contraste
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    
    # Mejorar brillo
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    
    # Mejorar saturación
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.1)
    
    # Mejorar nitidez
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)
    
    # Guardar imagen mejorada
    img.save(ruta_salida)

def hacer_upscale(img, factor=2):
    # Aumentar resolución (escala x2 con interpolación bicúbica)
    return cv2.resize(img, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)

def hacer_downscale(img, factor=0.25):
    # Obtener dimensiones originales
    height, width = img.shape[:2]
    
    # Calcular nuevas dimensiones
    new_width = int(width * factor)
    new_height = int(height * factor)
    
    # Reducir resolución usando INTER_AREA (mejor para reducción)
    return cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

# Solicitar carpeta de entrada al usuario
input_dir = input("Por favor, introduce la ruta de la carpeta con las imágenes a mejorar: ").strip()
if not os.path.exists(input_dir):
    print(f"❌ La carpeta '{input_dir}' no existe.")
    exit(1)

# Preguntar qué mejoras quiere aplicar
print("\nOpciones de escala:")
print("1. Upscale (aumentar tamaño)")
print("2. Downscale (reducir tamaño)")
print("3. Mantener tamaño original")
escala_opcion = input("Elige una opción (1/2/3): ").strip()

if escala_opcion == "1":
    hacer_upscale_resp = True
    hacer_downscale_resp = False
    factor = float(input("Factor de aumento (ej: 2 para doble tamaño): ").strip())
elif escala_opcion == "2":
    hacer_upscale_resp = False
    hacer_downscale_resp = True
    factor = float(input("Factor de reducción (ej: 0.25 para un cuarto del tamaño): ").strip())
else:
    hacer_upscale_resp = False
    hacer_downscale_resp = False
    factor = 1.0

hacer_autoenhance_resp = input("\n¿Quieres mejorar las fotos con autoenhance? (y/n): ").lower().strip()

if not hacer_upscale_resp and not hacer_downscale_resp and hacer_autoenhance_resp != 'y':
    print("❌ No se ha seleccionado ninguna mejora. Saliendo...")
    exit(1)

# Configura rutas
output_dir = "Output"             # Carpeta donde se guardarán las mejoradas
os.makedirs(output_dir, exist_ok=True)

print(f"\n📁 Carpeta de entrada: {input_dir}")
print(f"📁 Carpeta de salida: {output_dir}")

# Extensiones válidas
ext_validas = [".jpg", ".jpeg", ".png"]

# Contador de archivos procesados
total_archivos = 0
archivos_procesados = 0

# Proceso
print("\n🔍 Buscando imágenes...")
for nombre_archivo in os.listdir(input_dir):
    ruta_entrada = os.path.join(input_dir, nombre_archivo)
    nombre_base, ext = os.path.splitext(nombre_archivo)
    
    if ext.lower() not in ext_validas:
        print(f"⚠️  Ignorando archivo no válido: {nombre_archivo}")
        continue
    
    total_archivos += 1
    print(f"\n📸 Procesando: {nombre_archivo}")
    
    try:
        # Leer imagen
        img = cv2.imread(ruta_entrada)
        if img is None:
            print(f"❌ No se pudo leer: {nombre_archivo}")
            continue

        # Mostrar tamaño original
        height, width = img.shape[:2]
        print(f"📐 Tamaño original: {width}x{height}")

        # Aplicar upscale o downscale si se solicitó
        if hacer_upscale_resp:
            img = hacer_upscale(img, int(factor))
            print(f"✅ Upscale aplicado (factor: {factor})")
        elif hacer_downscale_resp:
            img = hacer_downscale(img, factor)
            print(f"✅ Downscale aplicado (factor: {factor})")

        # Mostrar nuevo tamaño
        new_height, new_width = img.shape[:2]
        print(f"📐 Nuevo tamaño: {new_width}x{new_height}")

        # Guardar temporalmente si necesitamos hacer autoenhance
        if hacer_autoenhance_resp == 'y':
            temp_path = os.path.join(output_dir, f"temp_{nombre_archivo}")
            cv2.imwrite(temp_path, img)
            print("✅ Imagen temporal guardada para autoenhance")
            
            # Aplicar autoenhance
            ruta_salida = os.path.join(output_dir, nombre_archivo)
            mejorar_imagen_autoenhance(temp_path, ruta_salida)
            print("✅ Autoenhance aplicado")
            
            # Eliminar archivo temporal
            os.remove(temp_path)
        else:
            # Si no hay autoenhance, guardar directamente
            ruta_salida = os.path.join(output_dir, nombre_archivo)
            cv2.imwrite(ruta_salida, img)

        print(f"✅ Procesado: {nombre_archivo}")
        archivos_procesados += 1
        
    except Exception as e:
        print(f"❌ Error procesando {nombre_archivo}: {str(e)}")
        continue

print(f"\n📊 Resumen:")
print(f"   - Total de archivos encontrados: {total_archivos}")
print(f"   - Archivos procesados con éxito: {archivos_procesados}")
print(f"   - Archivos ignorados: {total_archivos - archivos_procesados}")