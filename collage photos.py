import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import glob

# Rutas
base_dir = "."
fotos_dir = os.path.join(base_dir, "Fotos")
output_dir = os.path.join(base_dir, "Output")
csv_path = os.path.join(base_dir, "Lista alumnos.csv")
log_path = os.path.join(output_dir, "log_procesado.csv")
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Directorio de fotos: {fotos_dir}")
print(f"📁 Directorio de salida: {output_dir}")

# Dimensiones y márgenes
ANCHO_FINAL = 1920
ALTO_FINAL = 1080
MARGEN_INFERIOR = 0
MARGEN_LATERAL_TEXTO = 100

# Fuente para el texto (aún más grande)
try:
    fuente = ImageFont.truetype("arial.ttf", 110)
except:
    fuente = ImageFont.load_default()

# Leer CSV
print(f"📄 Leyendo archivo CSV: {csv_path}")
df = pd.read_csv(csv_path, sep=';')
log = []

# Procesar cada alumno
print("\n🔄 Procesando alumnos...")
for _, fila in df.iterrows():
    nombre = str(fila['Nombre']).strip()
    apellido1 = str(fila['Apellido 1']).strip()
    apellido2 = str(fila['Apellido 2']) if 'Apellido 2' in fila and pd.notna(fila['Apellido 2']) else ''
    apellido2 = apellido2.strip() if apellido2 else ''
    identificador = str(fila['N']).strip()
    if apellido2:
        nombre_completo = f"{nombre} {apellido1} {apellido2}"
    else:
        nombre_completo = f"{nombre} {apellido1}"
    
    print(f"\n👤 Procesando: {nombre_completo} (ID: {identificador})")

    # Buscar imágenes (cualquier combinación de extensiones)
    ruta_bf = ruta_af = None
    extensiones = ["jpg", "jpeg", "png"]
    for ext_bf in extensiones:
        bf = os.path.join(fotos_dir, f"{identificador}_bf.{ext_bf}")
        if os.path.exists(bf):
            ruta_bf = bf
            break
    for ext_af in extensiones:
        af = os.path.join(fotos_dir, f"{identificador}_af.{ext_af}")
        if os.path.exists(af):
            ruta_af = af
            break

    if ruta_bf and ruta_af:
        print(f"📸 Imágenes encontradas:")
        print(f"   - Antes: {ruta_bf}")
        print(f"   - Después: {ruta_af}")
    else:
        print(f"❌ No se encontraron las imágenes para {nombre_completo}")
        log.append({"N": identificador, "Nombre completo": nombre_completo, "Estado": "❌ Imágenes no encontradas"})
        continue

    try:
        # Cargar y escalar imágenes
        print("🖼️ Cargando y escalando imágenes...")
        img_bf = Image.open(ruta_bf)
        img_af = Image.open(ruta_af)

        # Corregir orientación usando EXIF si es necesario
        def corregir_orientacion(im):
            try:
                exif = im._getexif()
                if exif is not None:
                    orientation = exif.get(274)
                    if orientation == 3:
                        im = im.rotate(180, expand=True)
                    elif orientation == 6:
                        im = im.rotate(270, expand=True)
                    elif orientation == 8:
                        im = im.rotate(90, expand=True)
            except Exception:
                pass
            return im

        img_bf = corregir_orientacion(img_bf)
        img_af = corregir_orientacion(img_af)

        ANCHO_IMAGEN = ANCHO_FINAL // 2
        ALTO_IMAGEN = ALTO_FINAL  # Ahora es 1080 px exactos

        # Escalar para que el alto llene el canvas, sin recortar nada
        def escalar_sin_recorte(im):
            escala = ALTO_IMAGEN / im.height
            nuevo_ancho = int(im.width * escala)
            nuevo_alto = ALTO_IMAGEN
            im_redim = im.resize((nuevo_ancho, nuevo_alto), Image.LANCZOS)
            # Si el ancho es menor que la mitad, centrar en fondo blanco
            fondo_temp = Image.new("RGB", (ANCHO_IMAGEN, ALTO_IMAGEN), "white")
            x_offset = (ANCHO_IMAGEN - nuevo_ancho) // 2
            fondo_temp.paste(im_redim, (x_offset, 0))
            return fondo_temp

        img_bf = escalar_sin_recorte(img_bf)
        img_af = escalar_sin_recorte(img_af)

        # Crear fondo blanco
        fondo = Image.new("RGB", (ANCHO_FINAL, ALTO_FINAL), "white")
        draw = ImageDraw.Draw(fondo, "RGBA")

        # Pegar imágenes: cada una ocupa toda la altura y está centrada en su mitad
        fondo.paste(img_bf, (0, 0))
        fondo.paste(img_af, (ANCHO_FINAL // 2, 0))

        # --- Buscar fuente Arial como única opción ---
        posibles_fuentes = [
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Arial.ttf",
        ]
        font_path = None
        for fuente in posibles_fuentes:
            try:
                ImageFont.truetype(fuente, 40)
                font_path = fuente
                break
            except:
                continue
        if font_path:
            print(f"✅ Fuente utilizada: {font_path}")
        else:
            print("⚠️ No se encontró Arial. Se usará la fuente por defecto.")

        # --- Añadir cuadro de texto con nombre y apellidos ---
        texto = nombre_completo
        font_size = 100  # Tamaño inicial más pequeño
        fuente_temp = None
        aviso_fuente = False
        while font_size > 10:
            try:
                if font_path:
                    fuente_temp = ImageFont.truetype(font_path, font_size)
                else:
                    raise Exception("No font path")
            except:
                fuente_temp = ImageFont.load_default()
                aviso_fuente = True
            bbox = draw.textbbox((0, 0), texto, font=fuente_temp)
            ancho_texto = bbox[2] - bbox[0]
            if ancho_texto <= ANCHO_FINAL - 100:  # Solo 50px de margen a cada lado
                break
            font_size -= 2
        fuente_final = fuente_temp
        if aviso_fuente:
            print("⚠️ No se pudo cargar una fuente TrueType, usando fuente por defecto. El texto puede verse pequeño.")
        alto_texto = bbox[3] - bbox[1]
        x_texto = (ANCHO_FINAL - ancho_texto) // 2
        padding = 40
        margen_inferior_extra = 30
        # Calcular la altura total del cuadro
        altura_cuadro = alto_texto + padding + margen_inferior_extra
        y_texto = ALTO_FINAL - altura_cuadro  # Subir el cuadro para que no se salga
        box_coords = [
            x_texto - padding,
            y_texto - padding // 2,
            x_texto + ancho_texto + padding,
            y_texto + alto_texto + padding // 2 + margen_inferior_extra
        ]
        radio = 30
        grosor_borde = 6
        draw.rounded_rectangle(box_coords, radius=radio, fill=(255, 255, 255, 255), outline=(0, 102, 255), width=grosor_borde)
        draw.text((x_texto, y_texto), texto, fill="black", font=fuente_final)

        # Guardar imagen
        salida_path = os.path.join(output_dir, f"{identificador}_final.jpg")
        fondo.save(salida_path)
        print(f"✅ Collage guardado en: {salida_path}")
        log.append({"N": identificador, "Nombre completo": nombre_completo, "Estado": "✅ Procesado"})

    except Exception as e:
        print(f"❌ Error procesando {nombre_completo}: {str(e)}")
        log.append({"N": identificador, "Nombre completo": nombre_completo, "Estado": f"❌ Error: {e}"})

# Guardar log
pd.DataFrame(log).to_csv(log_path, index=False, encoding="utf-8")
print(f"\n📄 Log generado en: {log_path}")