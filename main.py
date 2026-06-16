from catalogo import Catalogo
from producto_alquiler import ProductoAlquiler
from datos_prueba import cargar_datos_prueba

def solicitar_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: Por favor, ingrese un número entero válido.")

def solicitar_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error: Por favor, ingrese un precio numérico válido.")

def main():
    mi_catalogo = Catalogo()
    cargar_datos_prueba(mi_catalogo)
    
    while True:
        print("\n" + "="*40)
        print(" SISTEMA DE VIDEOCLUB - GRUPO 9 ")
        print("="*40)
        print("1. Ver catálogo completo")
        print("2. Ver disponibles")
        print("3. Ver alquilados")
        print("4. Alquilar producto")
        print("5. Devolver producto")
        print("6. Agregar producto al catálogo")
        print("7. Eliminar producto")
        print("8. Buscar por tipo")
        print("9. Buscar por género")
        print("10. Proyección de ingresos")
        print("0. Salir del sistema")
        print("="*40)
        
        opcion = input("Seleccione una opción: ").strip()
        
        try:
            if opcion == "1":
                print("\n--- Catálogo Completo ---")
                if not mi_catalogo.productos:
                    print("El catálogo está vacío.")
                else:
                    for prod in mi_catalogo.productos:
                        print(prod)
                        
            elif opcion == "2":
                print("\n--- Productos Disponibles ---")
                mi_catalogo.listar_disponibles()
                
            elif opcion == "3":
                print("\n--- Productos Alquilados ---")
                mi_catalogo.listar_alquilados()
                
            elif opcion == "4":
                id_prod = solicitar_entero("Ingrese el ID del producto a alquilar: ")
                resultado = mi_catalogo.alquilar_producto(id_prod)
                print(f"¡Éxito! {resultado}")
                
            elif opcion == "5":
                id_prod = solicitar_entero("Ingrese el ID del producto a devolver: ")
                resultado = mi_catalogo.devolver_producto(id_prod)
                print(f"¡Éxito! {resultado}")
                
            elif opcion == "6":
                print("\n--- Carga de Nuevo Producto ---")
                id_prod = solicitar_entero("ID único: ")
                
                if any(p.id == id_prod for p in mi_catalogo.productos):
                    print("Error: Ya existe un producto con ese ID.")
                    continue
                    
                titulo = input("Título: ").strip()
                tipo = input("Tipo (videojuego/pelicula): ").strip().lower()
                if tipo not in ['videojuego', 'pelicula']:
                    print("Error: El tipo debe ser 'videojuego' o 'pelicula'.")
                    continue
                    
                plataforma = input("Plataforma (NES, SEGA, DVD, etc.): ").strip()
                genero = input("Género: ").strip()
                precio = solicitar_float("Precio de alquiler por día ($): ")
                
                nuevo_prod = ProductoAlquiler(id_prod, titulo, tipo, plataforma, genero, False, precio)
                mi_catalogo.agregarProducto(nuevo_prod)
                print(f"¡'{titulo}' fue agregado con éxito!")
                
            elif opcion == "7":
                id_prod = solicitar_entero("Ingrese el ID del producto a eliminar: ")
                mi_catalogo.eliminar_producto(id_prod)
                
            elif opcion == "8":
                tipo_busqueda = input("Ingrese tipo a buscar (videojuego/pelicula): ").strip()
                print(f"\n--- Resultados para Tipo: {tipo_busqueda} ---")
                mi_catalogo.buscar_por_tipo(tipo_busqueda)
                
            elif opcion == "9":
                genero_busqueda = input("Ingrese el género a buscar: ").strip()
                print(f"\n--- Resultados para Género: {genero_busqueda} ---")
                mi_catalogo.buscar_por_genero(genero_busqueda)
                
            elif opcion == "10":
                dias = solicitar_entero("Ingrese los días para proyectar los ingresos de lo alquilado: ")
                if dias < 0:
                    print("Error: Los días no pueden ser negativos.")
                else:
                    total = mi_catalogo.calcular_ingresos_estimados(dias)
                    print(f"\nIngresos totales estimados por {dias} días de alquiler: ${total:.2f}")
                    
            elif opcion == "0":
                print("\nSaliendo del sistema de gestión. ¡Hasta luego!")
                break
            else:
                print("Opción inválida. Seleccione un número del 0 al 10.")
                
        except KeyError as ke:
            print(f"Error de búsqueda: {ke}")
        except ValueError as ve:
            print(f"Error de negocio: {ve}")

if __name__ == "__main__":
    main()