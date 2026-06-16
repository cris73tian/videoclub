import json
import os
from producto_alquiler import ProductoAlquiler

class Catalogo:
    def __init__(self):
        self.productos = []
        self.ruta_json = "socios.json"
        # Carga automáticamente los socios guardados en el archivo JSON al arrancar
        self.miembros = self.cargar_socios_json()

    def cargar_socios_json(self):
        # Si el archivo JSON ya existe en la computadora, lee sus datos
        if os.path.exists(self.ruta_json):
            try:
                with open(self.ruta_json, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        # Si el archivo no existe o está vacío, arranca con los socios de prueba iniciales
        return [
            {"socio": "0001", "dni": "111", "nombre": "Cliente Habitual"},
            {"socio": "0002", "dni": "222", "nombre": "Gamer Pro"}
        ]

    def guardar_socios_json(self):
        # Guarda la lista de socios permanentemente en el archivo del disco duro
        with open(self.ruta_json, "w", encoding="utf-8") as f:
            json.dump(self.miembros, f, indent=4, ensure_ascii=False)

    def registrar_miembro(self, dni, nombre):
        # Validamos que el DNI no esté repetido antes de crear un número nuevo
        if any(m["dni"] == dni for m in self.miembros):
            raise ValueError("Este número de DNI ya está registrado como miembro.")
        
        # Calculamos el siguiente número correlativo basado en la cantidad actual
        siguiente_numero = len(self.miembros) + 1
        socio_id = f"{siguiente_numero:04d}"
        
        self.miembros.append({"socio": socio_id, "dni": dni, "nombre": nombre})
        
        # 💾 GUARDADO AUTOMÁTICO: Registramos el cambio en el archivo físico de inmediato
        self.guardar_socios_json()
        return f"Socio N° {socio_id} ({nombre}) registrado con éxito."

    def obtener_miembro_por_codigo(self, codigo_socio):
        for m in self.miembros:
            if m["socio"] == str(codigo_socio).strip():
                return m["nombre"]
        return None

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def eliminar_producto(self, id_producto):
        for producto in self.productos:
            if id_producto == producto.id:
                if producto.alquilado:
                    raise ValueError("No se puede eliminar un producto que está alquilado.")
                self.productos.remove(producto)
                print("Producto eliminado correctamente.")
                return
        raise KeyError("La ID es inexistente.")

    def alquilar_producto(self, id_producto, cliente):
        for producto in self.productos:
            if id_producto == producto.id:
                producto.alquilar(cliente)
                return f"El producto fue alquilado con éxito a {cliente}."
        raise KeyError("La ID es inexistente.")

    def devolver_producto(self, id_producto):
        for producto in self.productos:
            if id_producto == producto.id:
                producto.devolver()
                return "El producto fue devuelto."
        raise KeyError("La ID es inexistente.")

    def listar_disponibles(self):
        hay_stock = False
        for producto in self.productos:
            if producto.esta_disponible():
                print(producto.__str__())
                hay_stock = True
        if not hay_stock:
            print("No hay productos disponibles")

    def listar_alquilados(self):
        hay_alquilados = False
        for producto in self.productos:
            if producto.alquilado:
                print(producto.__str__())
                hay_alquilados = True
        if not hay_alquilados:
            print("No hay productos alquilados")

    def buscar_por_tipo(self, tipo_busqueda):
        encontrado = False
        for producto in self.productos:
            if producto.tipo == tipo_busqueda:
                print(producto)
                encontrado = True
        if not encontrado:
            print(f"No se encontraron productos del tipo '{tipo_busqueda}'.")

    def buscar_por_genero(self, genero_busqueda):
        encontrado = False
        for producto in self.productos:
            if genero_busqueda.lower() in producto.genero.lower():
                print(producto)
                encontrado = True
        if not encontrado:
            print(f"No se encontraron productos del género '{genero_busqueda}'.")

    def calcular_ingresos_estimados(self, dias):
        total = 0.0
        for producto in self.productos:
            if producto.alquilado:
                total += producto.ingreso_estimado(dias)
        return total
