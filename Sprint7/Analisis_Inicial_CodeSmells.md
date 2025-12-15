# Análisis Inicial de Code Smells
## Proyecto: Fundación Cudeca - Sistema Web de Gestión de Eventos

**Equipo Turing**  
**Sprint 7 - Análisis y Diseño de Aplicaciones**  
**Alumnos:** Samuel Fernández, Francisco Navarta  
**Fecha:** 10 de diciembre de 2025

---

## 1. Introducción

Este informe documenta los **code smells** que hemos encontrado en nuestra aplicación web después de implementar los patrones creacionales en Sprint 6. El objetivo es identificar qué problemas persisten en el código para poder refactorizarlo en futuros sprints.

### Contexto: Lo que hicimos en Sprint 6

En el Sprint 6 implementamos 5 patrones de diseño creacionales para mejorar cómo se crean los objetos en la aplicación:

- **Singleton** (AppConfig) - Para centralizar la configuración
- **Factory Method** (PaymentFactory) - Para los diferentes métodos de pago
- **Builder** (EventoBuilder) - Para construir eventos de forma más limpia
- **Abstract Factory** (TransactionFactory) - Para manejar entradas y boletos
- **Prototype** (clone()) - Para copiar eventos y rifas

Esto mejoró bastante la creación de objetos, pero nos dimos cuenta de que todavía hay varios problemas en el código que esos patrones no solucionan.

### Qué vamos a analizar

En este documento identificamos:
- **Code smells estructurales**: problemas con cómo está organizado el código
- **Code smells comportamentales**: problemas con quién hace qué
- **Problemas de diseño**: temas de seguridad y buenas prácticas

Los archivos que analizamos están en `SRC/baseDatos`:
- **Python:** `app.py` (586 líneas), `models.py`, `patterns.py`, `make_admin.py`
- **Templates:** 28 archivos HTML
- **Estáticos:** CSS e imágenes

---

## 2. Code Smells Estructurales

### 2.1 Long Method (Funciones Muy Largas)

**Nivel:** Alta prioridad

Tenemos varias funciones que son demasiado largas y hacen demasiadas cosas a la vez.

#### Problema 1: `participar_rifa()`
- **Dónde:** `SRC/baseDatos/app.py` líneas 96-134
- **Cuánto:** 39 líneas
- **Qué hace:**
  - Procesa pagos
  - Valida formularios
  - Crea registros en BD
  - Maneja errores

```python
@app.route('/rifa/<int:id>/participar', methods=['GET', 'POST'])
@login_required
def participar_rifa(id):
    # 39 líneas mezclando todo...
```

**Por qué es malo:** Es difícil de entender, testear y mantener. Si algo falla no sabemos dónde.

---

#### Problema 2: `pago_entrada()`
- **Dónde:** `SRC/baseDatos/app.py` líneas 136-181
- **Cuánto:** 46 líneas (¡la más larga!)
- **Problema:** Hace lo mismo que `participar_rifa()` pero para eventos

---

#### Problema 3: `donar()`
- **Dónde:** `SRC/baseDatos/app.py` líneas 451-483
- **Cuánto:** 33 líneas
- **Problema:** Maneja dos tipos de formularios diferentes en la misma función

---

### 2.2 Large Class (Archivo Gigante)

**Nivel:** Alta prioridad

**El problema:** `app.py` tiene **586 líneas** y hace de TODO:

- Login/registro/logout
- CRUD de eventos
- CRUD de rifas
- Gestión de socios
- Panel de admin
- Procesamiento de pagos
- Validación de QR codes

**Por qué es malo:**
- Violar el principio de "una clase, una responsabilidad"
- Difícil de navegar (demasiado scroll)
- Si tocas algo para eventos, podrías romper algo de rifas sin querer

---

### 2.3 Duplicated Code (Código Repetido)

**Nivel:** Media prioridad

Tenemos código que está repetido en varios lugares.

#### Duplicación 1: Procesamiento de pagos

Este código aparece 3 veces (líneas 106-111, 150-153, 464-469):

```python
processor = PaymentFactory.get_processor(metodo_pago)
if not processor:
    flash('Método de pago no válido')
    # return o redirect
success, msg = processor.process(monto, request.form)
```

**Problema:** Si queremos cambiar cómo procesamos pagos, tenemos que hacerlo en 3 sitios.

---

#### Duplicación 2: Borrar imágenes

Este código aparece 2 veces (líneas 258-264 y 415-421):

```python
if imagen_path:
    config = AppConfig()
    filename = os.path.basename(imagen_path)
    full_path = os.path.join(config.get_upload_folder, filename)
    if os.path.exists(full_path):
        try: os.remove(full_path)
        except: pass
```

---

### 2.4 Magic Numbers (Números sin Explicar)

**Nivel:** Media prioridad

Hay números en el código que no sabemos de dónde salen:

1. **Precio de boleto:** `10.0` en la línea 111 de app.py
   ```python
   processor.process(10.0 * cantidad_boletos, request.form)
   ```
   ¿Por qué 10.0? Debería ser una constante con nombre.

2. **Validación de tarjeta:** `{16}` en patterns.py línea 60
   ```python
   if not re.match(r'^\d{16}$', numero):
   ```

3. **CVV:** `{3}` en patterns.py línea 62

4. **DNI:** `% 23` en app.py línea 25

---

## 3. Code Smells Comportamentales

### 3.1 Feature Envy

**Nivel:** Media prioridad

**El problema:** La función `editar_evento()` está constantemente accediendo a `AppConfig` para guardar archivos.

```python
config = AppConfig()
filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
file.save(os.path.join(config.get_upload_folder, filename))
```

Este código se repite en `crear_evento()`, `crear_rifa()` y `editar_evento()`.

**Por qué es malo:** La lógica de subir archivos debería estar en su propia clase, no esparcida por todas partes.

---

### 3.2 Divergent Change

**Nivel:** Alta prioridad

**El problema:** La clase `Usuario` tiene demasiadas razones para cambiar.

```python
class Usuario(UserMixin, db.Model):
    # Datos personales
    nombre_usuario = ...
    correo_electronico = ...
    
    # Autenticación
    contrasena_hash = ...
    
    # Roles
    es_socio = ...
    admin_perfil = ...
    voluntario_perfil = ...
```

Si cambiamos cómo funciona la autenticación, cómo se gestionan los socios, o cómo funcionan los roles, siempre tocamos esta clase. Eso aumenta el riesgo de romper cosas.

---

### 3.3 Shotgun Surgery

**Nivel:** Alta prioridad

**El problema:** Para añadir un nuevo método de pago necesitamos tocar muchos archivos:

1. Crear `PaypalProcessor` en `patterns.py`
2. Añadirlo a `PaymentFactory`
3. Modificar 3 templates (pago_entrada.html, participar_rifa.html, donar.html)
4. Potencialmente las 3 funciones que procesan pagos

**Por qué es malo:** Un cambio "simple" requiere tocar 6+ archivos. Fácil olvidarse de alguno.

---

### 3.4 Data Clumps

**Nivel:** Media prioridad

Siempre vemos los mismos datos juntos:

**Grupos que se repiten:**
```python
# En varias funciones:
cantidad = request.form.get('cantidad')
metodo_pago = request.form.get('metodo_pago')

# En create_database_record:
id_evento, id_comprador, precio
id_rifa, id_comprador, precio
```

Estos datos deberían ir juntos en un objeto o clase.

---

### 3.5 Primitive Obsession

**Nivel:** Baja prioridad

La validación del DNI/NIE está implementada con strings y una función suelta:

```python
def validar_dni_nie(documento):
    documento = documento.upper().strip()
    if len(documento) != 9: return False
    # ... más lógica
```

Sería mejor tener una clase `DocumentoIdentidad` con métodos como `validar()`, `formatear()`, etc.

---

## 4. Problemas de Diseño

### 4.1 Empty Catch Blocks

**Nivel:** Alta prioridad (afecta debugging)

Tenemos bloques except que no hacen nada:

```python
try: 
    os.remove(image_path)
except: 
    pass
```

**Por qué es malo:** Si algo falla, no sabemos. Y no diferenciamos entre "el archivo no existe" (OK) y "no tengo permisos" (MAL).

---

### 4.2 Hardcoded Secrets

**Nivel:** CRÍTICA

```python
app.config['SECRET_KEY'] = 'tu_clave_secreta_muy_segura'
```

La clave secreta está en el código. Si alguien ve el repo, tiene acceso a la clave.

**Riesgo:** Session hijacking, CSRF attacks.

**Solución:** Usar variables de entorno.

---

### 4.3 Inline Styling

**Nivel:** Media prioridad

Hay estilos CSS mezclados en los HTML:

```html
<div style="display:inline-block;vertical-align:top;">
<a href="..." style="color: gold;">Admin</a>
```

Dificulta cambiar estilos y va contra separación de responsabilidades.

---

## 5. Resumen de Problemas Encontrados

| Code Smell | Tipo | Prioridad | Archivos |
|------------|------|-----------|----------|
| Long Method | Estructural | Alta | app.py |
| Large Class | Estructural | Alta | app.py |
| Duplicated Code | Estructural | Media | app.py |
| Magic Numbers | Estructural | Media | app.py, patterns.py |
| Feature Envy | Comportamental | Media | app.py |
| Divergent Change | Comportamental | Alta | models.py |
| Shotgun Surgery | Comportamental | Alta | varios |
| Data Clumps | Comportamental | Media | app.py |
| Empty Catch Blocks | Diseño | Alta | app.py |
| Hardcoded Secrets | Diseño | **CRÍTICA** | app.py |
| Inline Styling | Diseño | Media | templates |

---

## 6. Conclusiones

### Lo que funcionó bien (Sprint 6)

Los patrones creacionales que implementamos mejoraron bastante:
- Es más fácil añadir nuevos métodos de pago
- Crear eventos es más limpio con el Builder
- El código de creación de objetos está mejor organizado

### Lo que todavía necesita trabajo

Pero hay problemas que esos patrones no solucionaron:

1. **CRÍTICO - Seguridad:** La SECRET_KEY tiene que salir del código YA
2. **app.py es un monstruo:** 586 líneas haciendo de todo. Hay que dividirlo
3. **Código duplicado:** Especialmente en procesamiento de pagos
4. **Errores silenciados:** Los catch blocks vacíos nos están ocultando bugs

### Por qué los patrones creacionales no lo arreglaron todo

Los patrones que usamos en Sprint 6 solo mejoran **cómo se crean** los objetos. Los problemas que quedan necesitan:
- **Blueprints de Flask** para dividir app.py
- **Servicios** para centralizar lógica duplicada
- **Mejor manejo de errores**
- **Configuración segura**

### Próximos pasos

Para el siguiente sprint o futuras refactorizaciones deberíamos:

1. **Inmediato:** Mover SECRET_KEY a variables de entorno
2. **Dividir app.py** en módulos más pequeños usando Blueprints
3. **Crear servicios** para pagos y uploads de archivos
4. **Mejorar manejo de errores** (nada de except: pass)

---

**Fin del Análisis**
