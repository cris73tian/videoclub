import random
from producto_alquiler import ProductoAlquiler

def cargar_datos_prueba(catalogo):
    titulos_peliculas = [
        "El Padrino", "Volver al Futuro", "Star Wars", "Pulp Fiction",
        "Matrix", "El Señor de los Anillos", "Jurassic Park", "Batman",
        "Titanic", "Avatar", "Gladiador", "Inception", "Forrest Gump", "Terminator 2",
        "El Rey León", "Scarface"
    ]
    formatos_pelis = ["Blu-Ray", "DVD", "4K Ultra HD", "VHS"]
    generos_pelis = ["Drama", "Ciencia Ficción", "Acción", "Aventura", "Suspenso"]

    titulos_juegos = [
        "Super Mario Bros", "The Legend of Zelda", "Mortal Kombat", "Grand Theft Auto",
        "FIFA", "Resident Evil", "Minecraft", "Elden Ring", "Final Fantasy", "God of War",
        "Sonic the Hedgehog", "Pokémon", "Call of Duty", "Halo", "Tetris"
    ]
    plataformas_juegos = ["PS5", "Xbox Series X", "Nintendo Switch", "PC", "PS4", "Retro (NES/SEGA)"]
    generos_juegos = ["Plataformas", "Aventura", "Pelea", "Mundo Abierto", "Deportes", "Terror", "Estrategia"]

    contador_id = 1

    for titulo in titulos_peliculas:
        for i in range(10):
            formato = formatos_pelis[i % len(formatos_pelis)]
            genero = generos_pelis[(i + contador_id) % len(generos_pelis)]
            precio = round(random.uniform(2500.0, 5500.0), -2)
            
            # Corregido: Se pasa None en lugar de False para el control estricto de fechas y socios
            catalogo.agregar_producto(
                ProductoAlquiler(contador_id, titulo, 'pelicula', formato, genero, None, precio)
            )
            contador_id += 1

    for titulo in titulos_juegos:
        for i in range(10):
            plataforma = plataformas_juegos[i % len(plataformas_juegos)]
            genero = generos_juegos[(i + contador_id) % len(generos_juegos)]
            precio = round(random.uniform(4500.0, 9500.0), -2)
            
            ediciones = ["", " II", " III", " - Edición Especial", " Remake"]
            titulo_final = f"{titulo}{ediciones[i % len(ediciones)]}"
            
            # Corregido: Se pasa None en lugar de False para el control estricto de fechas y socios
            catalogo.agregar_producto(
                ProductoAlquiler(contador_id, titulo_final, 'videojuego', plataforma, genero, None, precio)
            )
            contador_id += 1

    print(f"✅ ¡Base de datos cargada con éxito! Se inyectaron {contador_id - 1} productos.")
