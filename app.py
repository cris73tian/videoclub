# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from catalogo import Catalogo
from datos_prueba import cargar_datos_prueba
from producto_alquiler import ProductoAlquiler

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_grupo_9'

# Inicializamos el catálogo y cargamos los datos automatizados
mi_catalogo = Catalogo()
cargar_datos_prueba(mi_catalogo)

# Agregar esto en app.py arriba de la ruta @app.route('/')
@app.context_processor
def utilidad_contexto():
    def filter_alquileres(productos, socio_id):
        # Filtra la lista de películas donde el socio_alquilado coincida con el ID buscado
        return [p for p in productos if str(p.socio_alquilado) == str(socio_id)]
    return dict(filter_alquileres=filter_alquileres)


@app.route('/')
def home():
    es_dueño = session.get('es_dueño', False)

    # === FILTROS DE PRODUCTOS ===
    tipo_filtro = request.args.get('tipo', '').strip()
    genero_filtro = request.args.get('genero', '').strip()
    estado_filtro = request.args.get('estado', '').strip()
    
    productos_a_mostrar = mi_catalogo.productos
    if tipo_filtro:
        productos_a_mostrar = [p for p in productos_a_mostrar if p.tipo == tipo_filtro.lower()]
    if genero_filtro:
        productos_a_mostrar = [p for p in productos_a_mostrar if genero_filtro.lower() in p.genero.lower()]
    if estado_filtro == 'disponible':
        productos_a_mostrar = [p for p in productos_a_mostrar if p.esta_disponible()]
    elif estado_filtro == 'alquilado':
        productos_a_mostrar = [p for p in productos_a_mostrar if p.alquilado is not None]

    # === FILTRO DE CLIENTES (NUEVO) ===
    buscar_cliente = request.args.get('buscar_cliente', '').strip().lower()
    socios_a_mostrar = mi_catalogo.miembros
    
    if buscar_cliente:
        # Filtra si el término coincide con el ID ('socio') o si está contenido en el nombre
        socios_a_mostrar = [
            s for s in socios_a_mostrar 
            if buscar_cliente in str(s.get('socio', '')).lower() or buscar_cliente in s.get('nombre', '').lower()
        ]

    # === PROYECCIÓN DE INGRESOS ===
    dias_proyeccion = request.args.get('dias', type=int)
    ingresos_estimados = None
    if es_dueño and dias_proyeccion and dias_proyeccion > 0:
        ingresos_estimados = mi_catalogo.calcular_ingresos_estimados(dias_proyeccion)

    total_clientes = len(mi_catalogo.miembros)

    return render_template('index.html', 
                           productos=productos_a_mostrar, 
                           ingresos=ingresos_estimados, 
                           dias_buscados=dias_proyeccion,
                           socios=socios_a_mostrar,        # Enviamos la lista filtrada de clientes
                           total_clientes=total_clientes,
                           es_dueño=es_dueño)

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password', '')
    if password == '0000':
        session['es_dueño'] = True
        flash("¡Bienvenido al Panel de Control, Dueño!", "exito")
    else:
        flash("Contraseña incorrecta. Acceso denegado.", "error")
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('es_dueño', None)
    flash("Sesión de dueño cerrada. Volviste al modo Cliente.", "exito")
    return redirect(url_for('home'))

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    if not session.get('es_dueño', False):
        flash("Error: Solo el dueño puede realizar esta acción.", "error")
        return redirect(url_for('home'))
        
    try:
        id_prod = int(request.form['id_producto'])
        titulo = request.form['titulo'].strip()
        tipo = request.form['tipo']
        plataforma = request.form['plataforma'].strip()
        genero = request.form['genero'].strip()
        precio = float(request.form['precio'])
        
        if any(p.id == id_prod for p in mi_catalogo.productos):
            flash(f"Error: Ya existe un producto con el ID {id_prod}.", "error")
            return redirect(url_for('home'))
            
        nuevo = ProductoAlquiler(id_prod, titulo, tipo, plataforma, genero, None, precio)
        mi_catalogo.agregar_producto(nuevo)
        flash(f"¡{titulo} agregado con éxito!", "exito")
    except Exception as e:
        flash(f"Error al cargar: {e}", "error")
    return redirect(url_for('home'))

@app.route('/eliminar_producto/<int:id_prod>')
def eliminar_producto(id_prod):
    if not session.get('es_dueño', False):
        flash("Error: Solo el dueño puede eliminar productos.", "error")
        return redirect(url_for('home'))
        
    for p in mi_catalogo.productos:
        if p.id == id_prod:
            if p.alquilado is not None:
                flash("No se puede eliminar un producto alquilado.", "error")
            else:
                mi_catalogo.productos.remove(p)
                flash("Producto eliminado correctamente.", "exito")
            return redirect(url_for('home'))
    flash("ID no encontrado.", "error")
    return redirect(url_for('home'))

@app.route('/registrar_socio', methods=['POST'])
def registrar_socio():
    if not session.get('es_dueño', False):
        flash("Error: Solo el dueño puede registrar clientes.", "error")
        return redirect(url_for('home'))
        
    dni = request.form['dni'].strip()
    nombre = request.form['nombre'].strip()
    try:
        mi_catalogo.registrar_miembro(dni, nombre)
        flash(f"Cliente {nombre} registrado.", "exito")
    except ValueError as e:
        flash(f"Error: {e}", "error")
    return redirect(url_for('home'))

@app.route('/eliminar_socio/<socio_id>')
def eliminar_socio(socio_id):
    if not session.get('es_dueño', False):
        flash("Error: Solo el dueño puede dar de baja clientes.", "error")
        return redirect(url_for('home'))
    
    # 1. Buscamos si el socio tiene películas alquiladas (usando la clave 'socio_alquilado')
    tiene_alquileres = any(str(p.socio_alquilado) == str(socio_id) for p in mi_catalogo.productos)
    if tiene_alquileres:
        flash("No se puede dar de baja al cliente porque tiene alquileres pendientes.", "error")
        return redirect(url_for('home'))
        
    # 2. Filtramos usando la clave correcta 'socio' que maneja tu archivo JSON
    mi_catalogo.miembros = [s for s in mi_catalogo.miembros if str(s.get('socio', '')) != str(socio_id)]
    
    # 3. Guardamos los cambios de forma persistente
    mi_catalogo.guardar_socios_json() 
    
    flash("Cliente dado de baja correctamente.", "exito")
    return redirect(url_for('home'))
    
    # Buscamos si el socio tiene películas alquiladas antes de borrarlo
    tiene_alquileres = any(p.socio_alquilado == socio_id for p in mi_catalogo.productos)
    if tiene_alquileres:
        flash("No se puede dar de baja al cliente porque tiene alquileres pendientes.", "error")
        return redirect(url_for('home'))
        
    # Filtramos la lista interna quitando al socio y guardamos en el JSON
    mi_catalogo.miembros = [s for s in mi_catalogo.miembros if s['socio_id'] != socio_id]
    mi_catalogo.guardar_socios_json() # Método de guardado persistente de tu catalogo.py
    flash("Cliente dado de baja correctamente.", "exito")
    return redirect(url_for('home'))

@app.route('/alquilar', methods=['POST'])
def alquilar():
    # Los clientes SÍ pueden alquilar directamente
    id_prod = int(request.form['id_producto'])
    num_socio = request.form['num_socio'].strip()
    
    nombre_socio = mi_catalogo.obtener_miembro_por_codigo(num_socio)
    if nombre_socio is None:
        flash(f"Error: El código de cliente '{num_socio}' no existe.", "error")
    else:
        for p in mi_catalogo.productos:
            if p.id == id_prod:
                try:
                    p.alquilar(num_socio, nombre_socio)
                    flash(f"¡Alquilado con éxito a {nombre_socio}!", "exito")
                except ValueError as e:
                    flash(f"Error: {e}", "error")
    return redirect(url_for('home'))

@app.route('/devolver', methods=['POST'])
def devolver():
    id_prod = int(request.form['id_producto'])
    for p in mi_catalogo.productos:
        if p.id == id_prod:
            try:
                recargo, dias = p.calcular_mora_producto()
                p.devolver()
                if recargo > 0:
                    flash(f"Devolución exitosa. Retraso: {dias} días. Multa: ${recargo:.2f}", "advertencia")
                else:
                    flash("Devuelto a tiempo sin penalizaciones.", "exito")
            except ValueError as e:
                flash(f"Error: {e}", "error")
    return redirect(url_for('home'))

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=10000)
