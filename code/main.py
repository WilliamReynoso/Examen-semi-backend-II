import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuración de la conexión a la base de datos
def get_db_connection():
    connection = psycopg2.connect(
        host="db",
        database="docker_postgres_dbex",
        user="postgres",
        password="password"
    )
    return connection

# Función para generar fechas de pago
def generar_fechas(frecuencia, fecha_inicio, fecha_fin):
    intervalo = {
        'Semanal': timedelta(weeks=1),
        'Mensual': timedelta(weeks=4),
        'Trimestral': timedelta(weeks=12),
        'Semestral': timedelta(weeks=26),
        'Anual': timedelta(days=365)
    }
    fecha_actual = fecha_inicio
    fechas = []
    while fecha_actual <= fecha_fin:
        # Si es domingo, mover al lunes
        if fecha_actual.weekday() == 6:
            fecha_actual += timedelta(days=1)
        fechas.append(fecha_actual)
        fecha_actual += intervalo[frecuencia]
    return fechas

# Endpoint para crear cliente y sus pagos
@app.route('/crear_cliente', methods=['POST'])
def crear_cliente():
    data = request.json
    nombre = data.get('nombre')
    email = data.get('email')
    fecha_inicio = datetime.strptime(data.get('fecha_inicio'), '%Y-%m-%d')
    fecha_fin = datetime.strptime(data.get('fecha_fin'), '%Y-%m-%d')
    cantidad = data.get('cantidad')
    frecuencia = data.get('frecuencia')
    
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        # Crear cliente
        cursor.execute("INSERT INTO clientes (nombre, email) VALUES (%s, %s) RETURNING id", (nombre, email))
        cliente_id = cursor.fetchone()['id']
        
        # Insertar pago y obtener ID
        cursor.execute("INSERT INTO pagos (cliente_id, cantidad, fecha_inicio, fecha_fin, frecuencia_pagos_id) "
                       "VALUES (%s, %s, %s, %s, (SELECT id FROM frecuencia_pagos WHERE frequencia=%s)) RETURNING id",
                       (cliente_id, cantidad, fecha_inicio, fecha_fin, frecuencia))
        pago_id = cursor.fetchone()['id']
        
        # Generar fechas de pago y guardarlas
        fechas = generar_fechas(frecuencia, fecha_inicio, fecha_fin)
        for fecha in fechas:
            cursor.execute("INSERT INTO fechas_pago (pago_id, fecha) VALUES (%s, %s)", (pago_id, fecha))
        
        conn.commit()
        return jsonify({"mensaje": "Cliente y pagos creados exitosamente"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@app.route('/pago', methods=['POST'])
def pagar():
    data = request.json
    nombre_cliente = data.get('nombre_cliente')
    num_pagos = int(data.get('num_pagos'))

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Obtener ID del cliente y de su pago pendiente
        cursor.execute("""
            SELECT p.id FROM pagos p
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.nombre = %s AND p.completado = false
        """, (nombre_cliente,))
        pago_id = cursor.fetchone()[0]
        
        # Actualizar `num_pagos` fechas de pago a pagado utilizando una subconsulta
        cursor.execute("""
            UPDATE fechas_pago SET pagado = true
            WHERE id IN (
                SELECT id FROM fechas_pago
                WHERE pago_id = %s AND pagado = false
                ORDER BY fecha ASC
                LIMIT %s
            )
        """, (pago_id, num_pagos))
        
        # Verificar si todas las fechas están pagadas
        cursor.execute("""
            SELECT COUNT(*) FROM fechas_pago
            WHERE pago_id = %s AND pagado = false
        """, (pago_id,))
        pendientes = cursor.fetchone()[0]
        
        if pendientes == 0:
            cursor.execute("UPDATE pagos SET completado = true WHERE id = %s", (pago_id,))
        
        conn.commit()
        return jsonify({"mensaje": "Pago aplicado exitosamente"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()


@app.route('/reporte/<string:nombre_cliente>', methods=['GET'])
def reporte(nombre_cliente):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
            SELECT f.fecha, f.pagado
            FROM fechas_pago f
            JOIN pagos p ON f.pago_id = p.id
            JOIN clientes c ON p.cliente_id = c.id
            WHERE c.nombre = %s
            ORDER BY f.fecha
        """, (nombre_cliente,))
        fechas = cursor.fetchall()
        
        return jsonify(fechas), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()