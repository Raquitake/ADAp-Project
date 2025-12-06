from app import app
from models import db, Usuario, Administrador

with app.app_context():
    # Buscar el usuario
    usuario = Usuario.query.filter_by(correo_electronico='ricardoallitt@gmail.com').first()
    
    if usuario:
        # Verificar si ya es admin
        if usuario.es_admin:
            print(f"✅ El usuario {usuario.nombre_usuario} ya es administrador")
        else:
            # Crear perfil de administrador
            admin = Administrador(id_usuario=usuario.id)
            db.session.add(admin)
            db.session.commit()
            print(f"✅ Usuario {usuario.nombre_usuario} convertido en administrador exitosamente!")
            print(f"   ID: {usuario.id}")
            print(f"   Email: {usuario.correo_electronico}")
    else:
        print("❌ No se encontró ningún usuario con ese correo")
        print("   Usuarios disponibles:")
        todos = Usuario.query.all()
        for u in todos:
            print(f"   - {u.correo_electronico}")
