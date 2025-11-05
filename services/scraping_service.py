# recetario-api/services/scraping_service.py

import requests
from bs4 import BeautifulSoup
import re # Importamos re para limpiar los ingredientes

def scrape_recetas_gratis(url: str):
    """
    Hace scraping de una URL específica de RecetasGratis.net para 
    extraer el título, las instrucciones y los ingredientes.
    """
    try:
        # 1. Descargar el HTML de la página
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # 2. Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # 3. Extraer los datos (específico de RecetasGratis.net)
        
        # --- Título ---
        titulo_tag = soup.find('h1', class_='titulo-receta')
        titulo = titulo_tag.text.strip() if titulo_tag else 'No se pudo encontrar el título'

        # --- Instrucciones ---
        # Las instrucciones están en divs con la clase 'apartado'
        instrucciones_divs = soup.find_all('div', class_='apartado')
        
        instrucciones_lista = []
        paso_num = 1
        for div in instrucciones_divs:
            # Buscamos el texto del paso
            paso_texto_tag = div.find(['p', 'li'])
            if paso_texto_tag:
                texto_limpio = paso_texto_tag.text.strip()
                if texto_limpio:
                    instrucciones_lista.append(f"{paso_num}. {texto_limpio}")
                    paso_num += 1
        
        instrucciones = "\n".join(instrucciones_lista)

        # --- Ingredientes ---
        # Los ingredientes están en 'label' dentro de un div con clase 'ingredientes'
        ingredientes_div = soup.find('div', class_='ingredientes')
        ingredientes_items = ingredientes_div.find_all('label') if ingredientes_div else []
        
        ingredientes = []
        for item in ingredientes_items:
            texto_completo = item.text.strip()
            
            # RecetasGratis tiene un formato como "1 Taza de Harina (150 gr)"
            # o "1 Cucharadita de Sal"
            # Vamos a intentar extraer la cantidad en gramos si está disponible
            
            nombre = texto_completo
            cantidad = 1.0
            unidad = 'gr' # Asumimos 'gr' por defecto

            # Intentamos extraer la cantidad en gramos (ej. "(150 gr)")
            match_gramos = re.search(r'\((\d+)\s*gr\)', texto_completo)
            
            if match_gramos:
                cantidad = float(match_gramos.group(1))
                # Limpiamos el nombre para quitarle la parte de los gramos
                nombre = re.sub(r'\((\d+)\s*gr\)', '', nombre).strip()
            else:
                # Si no hay gramos, intentamos estimar
                if 'cucharada' in nombre.lower():
                    cantidad = 15.0
                elif 'cucharadita' in nombre.lower():
                    cantidad = 5.0
                elif 'taza' in nombre.lower():
                    cantidad = 150.0
                elif 'kilo' in nombre.lower():
                    cantidad = 1000.0
                else:
                    # Para "1 Cebolla", estimamos 100g
                    cantidad = 100.0

            # Limpieza final del nombre
            nombre = re.sub(r'^\d+\s*(\w+\s*de)?\s*', '', nombre, count=1).strip()
            
            ingredientes.append({
                "nombre": nombre.capitalize(), # Capitalizamos el nombre
                "cantidad": round(cantidad, 2),
                "unidad": unidad
            })

        return {
            "titulo": titulo,
            "instrucciones": instrucciones,
            "ingredientes": ingredientes
        }

    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la URL: {e}")
        return None
    except Exception as e:
        print(f"Error al parsear el HTML: {e}")
        return None