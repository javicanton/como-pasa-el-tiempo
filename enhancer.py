import os
import cv2
from PIL import Image, ImageEnhance

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

def hacer_upscale(img):
    # Aumentar resolución (escala x2 con interpolación bicúbica)
    return cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# Solicitar carpeta de entrada al usuario
input_dir = input("Por favor, introduce la ruta de la carpeta con las imágenes a mejorar: ").strip()
if not os.path.exists(input_dir):
    print(f"❌ La carpeta '{input_dir}' no existe.")
    exit(1)

# Preguntar qué mejoras quiere aplicar
hacer_upscale_resp = input("\n¿Quieres hacer upscale de las imágenes? (y/n): ").lower().strip()
hacer_autoenhance_resp = input("¿Quieres mejorar las fotos con autoenhance? (y/n): ").lower().strip()

if hacer_upscale_resp != 'y' and hacer_autoenhance_resp != 'y':
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
    
    # Leer imagen
    img = cv2.imread(ruta_entrada)
    if img is None:
        print(f"❌ No se pudo leer: {nombre_archivo}")
        continue

    # Aplicar upscale si se solicitó
    if hacer_upscale_resp == 'y':
        img = hacer_upscale(img)
        print("✅ Upscale aplicado")

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

print(f"\n📊 Resumen:")
print(f"   - Total de archivos encontrados: {total_archivos}")
print(f"   - Archivos procesados con éxito: {archivos_procesados}")
print(f"   - Archivos ignorados: {total_archivos - archivos_procesados}")