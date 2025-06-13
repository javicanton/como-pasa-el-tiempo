from PIL import Image, ImageOps
import cv2
import numpy as np
import os
import random
from scipy.io import wavfile
import soundfile as sf
import subprocess

# Configuración
WIDTH, HEIGHT = 1920, 1080
FPS = 30
WAIT_DURATION = 5.0  # 5 segundos por foto
OUTPUT_FOLDER = "Output"
SHUTTER_SOUND_PATH = "shutter.mp3"
FLASH_DURATION = 0.2  # Restaurado a 0.2 segundos

# Solicitar al usuario la carpeta de entrada
print("\n=== Iniciando proceso de creación de animación ===")
INPUT_FOLDER = input("Por favor, introduce la ruta de la carpeta donde están las fotos: ").strip()
if not os.path.exists(INPUT_FOLDER):
    raise ValueError(f"La carpeta '{INPUT_FOLDER}' no existe.")

def load_images_with_frame():
    print("\nCargando imágenes...")
    images = []
    for fname in sorted(os.listdir(INPUT_FOLDER)):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"Procesando: {fname}")
            path = os.path.join(INPUT_FOLDER, fname)
            img = Image.open(path).convert("RGB")
            img = ImageOps.expand(img, border=20, fill='white')
            # Convertir PIL Image a numpy array para OpenCV
            img = np.array(img)
            # Convertir RGB a BGR (formato de OpenCV)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            images.append((fname, img))
    print(f"Total de imágenes cargadas: {len(images)}")
    # Mezclar aleatoriamente las imágenes
    random.shuffle(images)
    return images

def create_animation(images):
    if not images:
        raise ValueError("No se han encontrado imágenes en la carpeta especificada.")

    print("\nPreparando la animación...")
    # Calcular duración total
    total_frames = int(WAIT_DURATION * len(images) * FPS)
    print(f"Duración total: {total_frames/FPS:.1f} segundos")
    
    # Crear el video writer
    output_path = os.path.join(OUTPUT_FOLDER, "animacion_fotos.mp4")
    print(f"\nCreando video en: {output_path}")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS, (WIDTH, HEIGHT))

    # Preparar imágenes
    print("Preparando imágenes...")
    prepared_images = []

    for i, (name, img) in enumerate(images):
        print(f"Preparando imagen {i+1}/{len(images)}: {name}")
        
        # Asegurarnos de que la imagen quepa en la pantalla
        scale_w = (WIDTH - 100) / img.shape[1]  # Dejamos 50px de margen a cada lado
        scale_h = (HEIGHT - 100) / img.shape[0]  # Dejamos 50px de margen arriba y abajo
        scale = min(scale_w, scale_h, 1.0)  # No escalamos si la imagen es más pequeña
        
        if scale < 1.0:
            new_width = int(img.shape[1] * scale)
            new_height = int(img.shape[0] * scale)
            img = cv2.resize(img, (new_width, new_height))
        
        # Añadir borde blanco (estilo Polaroid)
        border = 20
        img_with_border = cv2.copyMakeBorder(
            img, border, border, border, border,
            cv2.BORDER_CONSTANT, value=(255, 255, 255)
        )
        
        # Calcular posición central
        center_x = (WIDTH - img_with_border.shape[1]) // 2
        center_y = (HEIGHT - img_with_border.shape[0]) // 2
        
        prepared_images.append((img_with_border, center_x, center_y, i * WAIT_DURATION))

    print("\nGenerando frames del video...")
    # Generar frames
    bar_length = 50  # Longitud de la barra de progreso
    for frame in range(total_frames):
        current_time = frame / FPS
        
        # Crear frame negro
        frame_img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        
        # Añadir cada imagen
        for img_with_border, center_x, center_y, start_time in prepared_images:
            if current_time >= start_time:
                # Añadir destello blanco solo para la imagen actual
                if current_time - start_time < FLASH_DURATION:
                    # Mantener las imágenes anteriores
                    for prev_img, prev_x, prev_y, prev_time in prepared_images:
                        if prev_time < start_time:
                            try:
                                frame_img[prev_y:prev_y + prev_img.shape[0], 
                                        prev_x:prev_x + prev_img.shape[1]] = prev_img
                            except ValueError:
                                pass
                    # Destello blanco
                    frame_img = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255
                else:
                    try:
                        frame_img[center_y:center_y + img_with_border.shape[0], 
                                center_x:center_x + img_with_border.shape[1]] = img_with_border
                    except ValueError:
                        pass  # Ignorar errores de tamaño
        
        # Escribir frame
        out.write(frame_img)
        
        # Mostrar barra de progreso
        if frame % 30 == 0 or frame == total_frames - 1:  # Actualizar cada segundo y en el último frame
            progress = (frame + 1) / total_frames  # Sumamos 1 para asegurar que llegue a 1.0
            filled_length = int(bar_length * progress)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            percent = progress * 100
            print(f'\rProgreso: |{bar}| {percent:.1f}%', end='', flush=True)
    
    print()  # Nueva línea al final

    # Liberar recursos
    print("\nFinalizando video...")
    out.release()
    
    # Añadir sonido si existe
    if os.path.exists(SHUTTER_SOUND_PATH):
        print("\nAñadiendo sonido al video...")
        try:
            # Crear una copia del video original
            backup_video = "backup_video.mp4"
            subprocess.run(['cp', output_path, backup_video], check=True)
            
            # Crear un archivo de audio temporal con silencio
            temp_audio = "temp_audio.wav"
            sample_rate = 44100
            total_duration = total_frames / FPS
            
            # Leer el sonido original para obtener el número de canales
            click_audio, click_sr = sf.read(SHUTTER_SOUND_PATH)
            num_channels = 2 if len(click_audio.shape) > 1 else 1
            
            # Crear silencio con el mismo número de canales que el sonido original
            silence = np.zeros((int(total_duration * sample_rate), num_channels))
            
            # Asegurarnos de que el click no sea más largo que FLASH_DURATION
            click_audio = click_audio[:int(FLASH_DURATION * click_sr)]
            
            # Resamplear si es necesario
            if click_sr != sample_rate:
                from scipy import signal
                click_audio = signal.resample(click_audio, int(len(click_audio) * sample_rate / click_sr))
            
            # Normalizar el audio del click
            click_audio = click_audio / np.max(np.abs(click_audio))
            
            # Añadir el sonido de click en cada transición
            for i in range(len(images)):
                click_time = i * WAIT_DURATION
                click_samples = int(click_time * sample_rate)
                # Añadir el click al silencio
                silence[click_samples:click_samples + len(click_audio)] = click_audio
            
            # Normalizar el audio final
            silence = silence / np.max(np.abs(silence))
            
            # Guardar el audio temporal
            sf.write(temp_audio, silence, sample_rate)
            
            # Combinar video y audio usando ffmpeg
            temp_output = "temp_output.mp4"
            print("Combinando video y audio...")
            subprocess.run([
                'ffmpeg', '-i', backup_video, '-i', temp_audio,
                '-c:v', 'copy', '-c:a', 'aac', '-map', '0:v', '-map', '1:a',
                '-shortest', temp_output
            ], check=True)
            
            # Verificar que el nuevo archivo tiene un tamaño razonable
            if os.path.getsize(temp_output) > os.path.getsize(backup_video) * 0.5:  # Al menos 50% del tamaño original
                os.replace(temp_output, output_path)
                print("Audio añadido correctamente")
            else:
                print("Error: El video resultante es demasiado pequeño. Manteniendo el video original.")
                os.remove(temp_output)
            
            # Limpiar archivos temporales
            os.remove(temp_audio)
            os.remove(backup_video)
        except Exception as e:
            print(f"No se pudo añadir el audio: {e}")
            print("Manteniendo el video original sin audio.")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_FOLDER):
        print(f"\nCreando carpeta de salida: {OUTPUT_FOLDER}")
        os.makedirs(OUTPUT_FOLDER)

    images = load_images_with_frame()
    create_animation(images)
    print("\n=== ¡Video creado exitosamente! ===")