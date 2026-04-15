#!/usr/bin/env python
import os
import sys

os.chdir(r"c:\Users\10443855617\Desktop\dev-web")
sys.path.insert(0, r"c:\Users\10443855617\Desktop\dev-web")

print("Testando setup...")
try:
    from app import app, db
    from models.usuario_models import Usuario
    
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        print("✓ Tabelas criadas")
        
        # Verificar admin
        admin = Usuario.query.filter_by(email="admin@seloedu.com").first()
        if admin:
            print(f"✓ Admin existe: {admin.name}")
        else:
            print("✗ Admin não encontrado - será criado")
    
    print("\n✓ Setup OK! Inicie com: python app.py")
    print("App estará em: http://localhost:5000")
    
except Exception as e:
    print(f"✗ ERRO: {e}")
    import traceback
    traceback.print_exc()
