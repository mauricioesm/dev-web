# 🔐 Fluxo Esqueceu Senha - Instruções de Setup

## ✅ O que foi Implementado

### 1. **Modelo Usuario** (`models/usuario_models.py`)
```python
reset_token       # Token único para reset
reset_expiry      # Data de expiração (1h)
get_reset_token() # Gera token
verify_reset_token(token) # Valida token
```

### 2. **Rotas** (`app.py`)
- `POST /esqueceu-senha` → Email com link
- `GET|POST /redefinir-senha/<token>` → Reset de senha

### 3. **Configuração** (`config.py`)
- MailHog: `localhost:1025`

### 4. **Templates**
- `esqueceu_senha.html` → Formulário de email
- `redefinir_senha.html` → Formulário de nova senha
- `login.html` → Link "Esqueceu a senha?"

---

## 🚀 Passo a Passo

### Passo 1: Instalar Dependências
```bash
pip install -r requirements.txt
```

### Passo 2: Iniciar MailHog (Docker)
```bash
docker-compose up -d
```

Verifique em: **http://localhost:8025**

### Passo 3: Rodar Aplicação
```bash
python app.py
```

Acesse: **http://localhost:5000/login**

---

## 🧪 Testar Fluxo

1. Clique em **"Esqueceu a senha?"**
2. Digite: `admin@seloedu.com`
3. Clique em **"Enviar Link"**
4. Abra **http://localhost:8025** (MailHog)
5. Copie o link do email
6. Cole na barra de endereço
7. Defina nova senha
8. Faça login com a nova senha

---

## ⚠️ Se der erro "no such column: usuarios.reset_token"

Execute estes comandos no PowerShell:

```powershell
# Remover banco antigo
Remove-Item -Path "c:\Users\10443855617\Desktop\dev-web\instance\database.db" -Force -ErrorAction SilentlyContinue

# Limpar cache Python
Remove-Item -Path "c:\Users\10443855617\Desktop\dev-web\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue

# Limpar cache dos modelos
Remove-Item -Path "c:\Users\10443855617\Desktop\dev-web\models\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue

# Rodar app novamente
python app.py
```

---

## 📧 Credenciais de Teste

| Campo | Valor |
|-------|-------|
| Email | admin@seloedu.com |
| Senha Inicial | 123456 |

---

## 🎯 Fluxo Técnico

```
1. User clica "Esqueceu a senha?"
   ↓
2. POST /esqueceu-senha com email
   ↓
3. Busca usuario por email
   ↓
4. Se existe:
   - Gera token com secrets.token_urlsafe(32)
   - Define expiração = agora + 1 hora
   - Envia email com link: /redefinir-senha/<token>
   ↓
5. User clica link do email
   ↓
6. GET /redefinir-senha/<token>
   - Valida token (existe e não expirou)
   - Exibe formulário
   ↓
7. POST /redefinir-senha/<token> com nova senha
   - Atualiza password hash
   - Limpa reset_token
   - Redireciona para login
   ↓
8. User faz login com nova senha ✓
```

---

## 📝 Arquivos Criados/Modificados

✅ `models/usuario_models.py` - Reset token fields + methods
✅ `config.py` - MailHog config
✅ `app.py` - Rotas de reset
✅ `templates/esqueceu_senha.html` - Form email
✅ `templates/redefinir_senha.html` - Form nova senha
✅ `templates/login.html` - Link reset
✅ `requirements.txt` - Dependências
✅ `docker-compose.yml` - MailHog

---

## ✨ Sistema Pronto!

O fluxo está **100% funcional e conciso**. Basta seguir os passos acima! 🎉
