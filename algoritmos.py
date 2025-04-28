import pygame
import sys
import time

# Inicializar PyGame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 900, 700 # Ajustado un poco el tamaño
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Búsqueda Binaria Animada")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)  # Rango activo
RED = (255, 99, 71)    # Punto medio
GREEN = (50, 205, 50)  # Encontrado
GRAY = (169, 169, 169)  # Descartado
YELLOW = (255, 255, 0)  # Color alternativo (no usado actualmente, pero útil)

# Fuente
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Datos del algoritmo
arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91] # Agregados más elementos para mejor visualización
target = 23
left = 0
right = len(arr) - 1
found = -1
mid = -1 # Variable para almacenar el índice del medio actual
current_step_text = "Presiona SPACE para iniciar la búsqueda..."
speed_ms = 1000  # Milisegundos entre pasos (1 segundo)

# Estados de la animación
STATE_IDLE = 0
STATE_SEARCHING = 1
STATE_FOUND = 2
STATE_NOT_FOUND = 3
current_state = STATE_IDLE

# Evento de temporizador personalizado para el siguiente paso del algoritmo
NEXT_STEP_EVENT = pygame.USEREVENT + 1

# --- Funciones del Algoritmo ---

def reset_search():
    """Reinicia los parámetros de búsqueda."""
    global left, right, found, mid, current_step_text, current_state
    left = 0
    right = len(arr) - 1
    found = -1
    mid = -1
    current_step_text = f"Buscando {target} en el arreglo..."
    current_state = STATE_SEARCHING
    # Inicia el temporizador para el primer paso
    pygame.time.set_timer(NEXT_STEP_EVENT, speed_ms)

def perform_step():
    """Ejecuta un solo paso del algoritmo de búsqueda binaria."""
    global left, right, found, mid, current_step_text, current_state

    if current_state != STATE_SEARCHING:
        # Si no estamos buscando, no hacer nada
        return

    if left <= right:
        mid = (left + right) // 2
        mid_value = arr[mid]

        current_step_text = f"Paso: left={left}, right={right}, mid={mid}. Valor en mid: {mid_value}"

        if mid_value == target:
            found = mid
            current_step_text = f"¡Encontrado! El objetivo {target} está en el índice {found}."
            current_state = STATE_FOUND
            pygame.time.set_timer(NEXT_STEP_EVENT, 0) # Detiene el temporizador
        elif mid_value < target:
            current_step_text += f". {mid_value} < {target}. Descartando la mitad izquierda."
            left = mid + 1
        else: # mid_value > target
            current_step_text += f". {mid_value} > {target}. Descartando la mitad derecha."
            right = mid - 1

    else: # left > right
        found = -1
        current_step_text = f"El objetivo {target} no se encontró en el arreglo."
        current_state = STATE_NOT_FOUND
        pygame.time.set_timer(NEXT_STEP_EVENT, 0) # Detiene el temporizador

# --- Funciones de Dibujo ---

def draw_array():
    """Dibuja las barras del arreglo y sus valores."""
    bar_width = 60
    bar_spacing = 15
    total_bar_width = (bar_width + bar_spacing) * len(arr) - bar_spacing
    start_x = (WIDTH - total_bar_width) // 2
    base_y = HEIGHT - 250 # Posición base para las barras

    # Dibujar barras y números
    for i in range(len(arr)):
        x = start_x + i * (bar_width + bar_spacing)
        bar_height = arr[i] * 5 # Escalar el valor para la altura de la barra (ajustado escala)

        color = GRAY  # Por defecto: descartado (fuera del rango inicial o ya pasado)

        if left <= i <= right and current_state == STATE_SEARCHING:
             color = BLUE  # Rango activo actual de la búsqueda
        elif found != -1 and i == found:
             color = GREEN # Elemento encontrado

        # Dibujar la barra
        pygame.draw.rect(screen, color, (x, base_y - bar_height, bar_width, bar_height))
        pygame.draw.rect(screen, BLACK, (x, base_y - bar_height, bar_width, bar_height), 2) # Borde

        # Dibujar el valor dentro de la barra
        value_text = small_font.render(str(arr[i]), True, BLACK)
        text_rect = value_text.get_rect(center=(x + bar_width // 2, base_y - bar_height // 2))
        screen.blit(value_text, text_rect)

        # Dibujar el índice debajo de la barra
        index_text = small_font.render(str(i), True, BLACK)
        index_rect = index_text.get_rect(center=(x + bar_width // 2, base_y + 20))
        screen.blit(index_text, index_rect)

    # Resaltar left, right y mid
    if current_state == STATE_SEARCHING or current_state == STATE_FOUND:
        # Dibujar indicadores de left, right
        if left <= len(arr): # Asegurarse de que left está dentro de los límites lógicos
             left_x = start_x + left * (bar_width + bar_spacing) + bar_width // 2
             pygame.draw.line(screen, BLACK, (left_x, base_y + 30), (left_x, base_y + 50), 2)
             left_text = small_font.render("left", True, BLACK)
             screen.blit(left_text, (left_x - left_text.get_width() // 2, base_y + 55))

        if right >= -1: # Asegurarse de que right está dentro de los límites lógicos
             right_x = start_x + right * (bar_width + bar_spacing) + bar_width // 2
             pygame.draw.line(screen, BLACK, (right_x, base_y + 30), (right_x, base_y + 50), 2)
             right_text = small_font.render("right", True, BLACK)
             screen.blit(right_text, (right_x - right_text.get_width() // 2, base_y + 55))

        # Dibujar indicador de mid solo si es válido
        if mid != -1 and left <= right: # mid es válido solo si left <= right
             mid_x = start_x + mid * (bar_width + bar_spacing) + bar_width // 2
             pygame.draw.line(screen, RED, (mid_x, base_y + 70), (mid_x, base_y + 90), 3)
             mid_text = small_font.render("mid", True, RED)
             screen.blit(mid_text, (mid_x - mid_text.get_width() // 2, base_y + 95))


def draw_ui():
    """Dibuja el texto de explicación y la leyenda."""
    # Explicación paso a paso
    step_surface = font.render(current_step_text, True, BLACK)
    screen.blit(step_surface, (50, 50))

    # Leyenda de colores
    legend_start_y = HEIGHT - 150
    legend_spacing = 30

    pygame.draw.rect(screen, BLUE, (50, legend_start_y, 20, 20))
    screen.blit(small_font.render("Rango activo (left a right)", True, BLACK), (80, legend_start_y))

    pygame.draw.rect(screen, RED, (50, legend_start_y + legend_spacing, 20, 20))
    screen.blit(small_font.render("Punto medio (mid)", True, BLACK), (80, legend_start_y + legend_spacing))

    pygame.draw.rect(screen, GREEN, (50, legend_start_y + 2 * legend_spacing, 20, 20))
    screen.blit(small_font.render("Elemento encontrado", True, BLACK), (80, legend_start_y + 2 * legend_spacing))

    pygame.draw.rect(screen, GRAY, (50, legend_start_y + 3 * legend_spacing, 20, 20))
    screen.blit(small_font.render("Descartado / Fuera de rango activo", True, BLACK), (80, legend_start_y + 3 * legend_spacing))

    # Instrucciones
    if current_state == STATE_IDLE:
        instruction_text = small_font.render("Presiona SPACE para iniciar la búsqueda.", True, BLACK)
        screen.blit(instruction_text, (50, 100))
    elif current_state in [STATE_FOUND, STATE_NOT_FOUND]:
         instruction_text = small_font.render("Presiona SPACE para reiniciar.", True, BLACK)
         screen.blit(instruction_text, (50, 100))


# Bucle principal
running = True
clock = pygame.time.Clock() # Para controlar la velocidad de fotogramas

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_state in [STATE_IDLE, STATE_FOUND, STATE_NOT_FOUND]:
                    reset_search()
        if event.type == NEXT_STEP_EVENT:
            # Este evento se dispara cuando el temporizador llega a cero
            perform_step()

    # Dibujar todo en cada fotograma
    screen.fill(WHITE)
    draw_array()
    draw_ui()

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de fotogramas
    clock.tick(60) # Limitar a 60 fotogramas por segundo (la animación se controla por el temporizador, esto es para la fluidez general)

pygame.quit()
sys.exit()