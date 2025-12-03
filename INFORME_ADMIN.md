# Informe de Implementación: Vistas de Administrador

**Autor:** Samuel  
**Fecha:** 3 de diciembre de 2025  
**Rama:** Samuel

---

## Resumen Ejecutivo

Se ha implementado un sistema completo de administración para la página web de la Fundación Cudeca. Los administradores ahora pueden gestionar eventos (crear, editar, eliminar) y visualizar la lista de socios desde interfaces dedicadas.

---

## Cambios Realizados

### 1. Backend (app.py)

#### Decorador de Seguridad
Se creó un decorador `@admin_required` que:
- Verifica si el usuario está autenticado
- Comprueba si tiene permisos de administrador (`current_user.es_admin`)
- Devuelve error 403 (Prohibido) si no cumple los requisitos

#### Nuevas Rutas de Administración
Se añadieron 4 rutas protegidas:

| Ruta | Método | Función |
|------|--------|---------|
| `/admin/evento/crear` | GET, POST | Crear nuevos eventos |
| `/admin/evento/editar/<id>` | GET, POST | Editar eventos existentes |
| `/admin/evento/eliminar/<id>` | POST | Eliminar eventos |
| `/admin/socios` | GET | Ver lista de socios |

Todas estas rutas están protegidas con `@login_required` y `@admin_required`.

---

### 2. Frontend - Interfaz de Usuario

#### Navbar (base.html)
- Se añadió un enlace "🛠️ Admin" en color dorado
- Solo visible para usuarios administradores
- Lleva directamente a la gestión de socios

#### Dashboard (dashboard.html)
**Cambios en el perfil:**
- Badge "⭐ Administrador" junto al estado de socio

**Nuevo panel de administración:**
- Botón "➕ Crear Evento"
- Botón "👥 Gestionar Socios"
- Botón "📋 Ver Todos los Eventos"

#### Página de Eventos (eventos.html)
**En la cabecera:**
- Botón "➕ Crear Evento" (flotante a la derecha)

**En cada tarjeta de evento:**
- Botón "✏️ Editar" (amarillo)
- Botón "🗑️ Eliminar" (rojo, con confirmación)

---

### 3. Nuevas Plantillas de Administración

Se creó el directorio `templates/admin/` con tres archivos:

#### crear_evento.html
Formulario para crear eventos con campos:
- Nombre del evento
- Localización
- Fecha y hora
- Información adicional

#### editar_evento.html
Formulario pre-rellenado para modificar eventos existentes.

#### gestionar_socios.html
Tabla con todos los socios mostrando:
- ID
- Nombre
- Email
- DNI/NIF

---

## Aspectos Técnicos

### Seguridad
- Todas las rutas de administración requieren autenticación
- Doble verificación: `@login_required` + `@admin_required`
- Los usuarios normales reciben error 403 si intentan acceder directamente

### Renderizado Condicional
Se utiliza la propiedad `current_user.es_admin` para mostrar/ocultar elementos:
```html
{% if current_user.is_authenticated and current_user.es_admin %}
    <!-- Contenido solo para admins -->
{% endif %}
```

### Modelo de Datos
Se aprovecha la relación existente entre `Usuario` y `Administrador`:
- La propiedad `Usuario.es_admin` verifica si existe un registro en `Administrador`
- No se modificó el modelo de base de datos

---

## Cómo Crear un Administrador

Para convertir un usuario en administrador, ejecutar en consola Python:

```python
from models import db, Administrador

# Suponiendo que el usuario tiene ID=1
admin = Administrador(id_usuario=1)
db.session.add(admin)
db.session.commit()
```

---

## Pruebas Recomendadas

### Como Usuario Normal
1. Iniciar sesión con cuenta regular
2. Verificar que NO aparecen botones de administración
3. Intentar acceder a `/admin/evento/crear` → Debe mostrar error 403

### Como Administrador
1. Iniciar sesión con cuenta de administrador
2. Verificar enlace "🛠️ Admin" en navbar
3. Verificar badge "⭐ Administrador" en dashboard
4. Verificar panel de administración en dashboard
5. Ir a Eventos → Verificar botón "Crear Evento"
6. Verificar botones "Editar" y "Eliminar" en cada evento
7. Probar crear un evento nuevo
8. Probar editar un evento existente
9. Probar eliminar un evento (verificar confirmación)
10. Acceder a "Gestionar Socios" → Verificar tabla

---

## Archivos Modificados

```
SRC/baseDatos/
├── app.py                                    [MODIFICADO]
└── templates/
    ├── base.html                             [MODIFICADO]
    ├── dashboard.html                        [MODIFICADO]
    ├── eventos.html                          [MODIFICADO]
    └── admin/                                [NUEVO DIRECTORIO]
        ├── crear_evento.html                 [NUEVO]
        ├── editar_evento.html                [NUEVO]
        └── gestionar_socios.html             [NUEVO]
```

---

## Estado del Proyecto

✅ Implementación completa  
✅ Código commiteado en rama `Samuel`  
✅ Listo para merge con `main`  
⚠️ Requiere crear usuarios administradores manualmente en BD

---

## Notas Adicionales

- El diseño respeta el estilo existente del proyecto
- Se utilizan las clases CSS ya definidas (btn-yellow, btn-green, etc.)
- Compatible con el sistema de autenticación actual (Flask-Login)
- No se modificó la estructura de la base de datos
