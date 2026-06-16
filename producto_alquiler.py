import datetime

class ProductoAlquiler:
    def __init__(self, id_producto, titulo, tipo, plataforma, genero, alquilado, precio_alquiler):
        self.id = int(id_producto)
        self.titulo = str(titulo)
        self.tipo = str(tipo)
        self.plataforma = str(plataforma)
        self.genero = str(genero)
        
        # Guardará el NÚMERO de socio que alquiló (ej: "0001") o None si está libre
        self.socio_alquilado = None
        # Guardará el NOMBRE de la persona para mostrarlo en el catálogo público
        self.alquilado = None
        self.fecha_alquiler = None
        self.fecha_vencimiento = None
        
        self.precio_alquiler = float(precio_alquiler)

    def alquilar(self, numero_socio, nombre_socio):
        if self.alquilado:
            raise ValueError("El producto ya se encuentra alquilado.")
        self.socio_alquilado = str(numero_socio)
        self.alquilado = str(nombre_socio)
        self.fecha_alquiler = datetime.date.today()
        # Plazo estricto de 3 días para su devolución
        self.fecha_vencimiento = self.fecha_alquiler + datetime.timedelta(days=3)

    def devolver(self):
        if not self.alquilado:
            raise ValueError("El producto no estaba alquilado.")
        self.socio_alquilado = None
        self.alquilado = None
        self.fecha_alquiler = None
        self.fecha_vencimiento = None

    def esta_disponible(self):
        return self.alquilado is None

    def calcular_mora_producto(self):
        """Calcula los días de atraso y el recargo del 20% diario si corresponde"""
        if not self.fecha_vencimiento or not self.alquilado:
            return 0.0, 0
        hoy = datetime.date.today()
        if hoy > self.fecha_vencimiento:
            dias_atraso = (hoy - self.fecha_vencimiento).days
            # Recargo del 20% del valor de alquiler por cada día de retraso
            recargo_total = (self.precio_alquiler * 0.20) * dias_atraso
            return recargo_total, dias_atraso
        return 0.0, 0

    def ingreso_estimado(self, dias):
        return self.precio_alquiler * int(dias)

    def __str__(self):
        estado = f"Alquilado por: {self.alquilado}" if self.alquilado else "Disponible"
        return f"ID: {self.id} | {self.titulo} ({self.tipo.capitalize()}) | Estado: {estado}"