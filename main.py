import math
import flet as ft
import random

def generate_random_color():
    """Generate a random hex color."""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    if isinstance(hex_color, tuple):
        raise ValueError("Expected a hex color string, but received a tuple.")
    
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def color_similarity_percentage(hex_color1, hex_color2):
    """Compare two hex colors and return the accuracy percentage of the second color from the first one."""
    rgb1 = hex_to_rgb(hex_color1)
    rgb2 = hex_to_rgb(hex_color2)
    
    # Calculate Euclidean distance between the two colors
    distance = math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(rgb1, rgb2)))
    
    # Maximum possible distance in RGB space
    max_distance = math.sqrt(3 * (255 ** 2))
    
    # Calculate similarity percentage
    similarity = ((max_distance - distance) / max_distance) * 100
    
    return round(similarity, 2)

def on_submit_color(e):
    first_color = color_box.controls[0].bgcolor
    second_color = "#" + color_input.value
    

    percentage = color_similarity_percentage(first_color, second_color)
    score_text.value = percentage
    score_text.update()
    color_box.controls[1].bgcolor = second_color
    color_box.update()
    
def input_check(e):
    # Limit input to 6 characters and only allow 0-9, a-f
    if len(e.control.value) > 6 or not all(c in '0123456789abcdef' for c in e.control.value.lower()):
        e.control.error_text = "Input must be up to 6 characters and contain only 0-9, a-f"
        e.control.update()
    else:
        e.control.error_text = None
        e.control.update()

def main(page: ft.Page):
    global title, color_box, color_input, submit_button, page_main, score_text
    page.title = "Color Trainer"
    page.window.width = 500
    page.window.height = 500
    page.theme_mode = ft.ThemeMode.LIGHT
    
    title = ft.Text(page.title, size=40)
    color_box = ft.Row([
                    ft.Container(height=100, width=100, bgcolor=generate_random_color(), border_radius=20),
                    ft.Container(height=100, width=100, bgcolor="#ababab", border_radius=20)
                ])
    color_input = ft.TextField(label="Input Color HEX", border=ft.InputBorder.NONE, bgcolor="#eeeeee", border_radius=20, max_length=6, on_change=input_check)
    submit_button = ft.ElevatedButton("Submit", on_click=on_submit_color)
    score_text = ft.Text(size=24)

    page_main = ft.Container(
        width=500,
        height=500,
        content=ft.Column([
            # title,
            color_box,
            score_text,
            ft.Column([color_input, submit_button]),
        ])   
    )  
    page.controls.append(page_main)
    page.update()

ft.app(target=main)