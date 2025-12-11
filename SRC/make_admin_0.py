from app import app
from models import db, Usuario, Administrador
from werkzeug.security import generate_password_hash

with app.app_context():
    # 1. Buscar o crear el usuario
    correo = 'conejo@gmail.com'
    usuario = Usuario.query.filter_by(correo_electronico=correo).first()
    
    if not usuario:
        print(f"ℹ️ El usuario {correo} no existe. Creándolo...")
        hashed_password = generate_password_hash('conejo', method='pbkdf2:sha256')
        usuario = Usuario(
            nombre_usuario=correo.split('@')[0],
            correo_electronico=correo,
            contrasena_hash=hashed_password,
            es_socio=False
        )
        db.session.add(usuario)
        db.session.commit()
        print(f"✅ Usuario 'conejo' creado exitosamente.")
    else:
        print(f"ℹ️ El usuario {correo} ya existe.")

    # 2. Hacerlo administrador
    if usuario.es_admin:
        print(f"✅ El usuario ya es administrador.")
    else:
        print("ℹ️ Asignando permisos de administrador...")
        admin = Administrador(id_usuario=usuario.id)
        db.session.add(admin)
        db.session.commit()
        print(f"✅ ¡Usuario {usuario.nombre_usuario} ahora es administrador!")

    print("-" * 30)
    print("Credenciales:")
    print(f"Email: {correo}")
    print(f"Pass:  conejo")
