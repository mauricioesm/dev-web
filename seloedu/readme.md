# dev-web

Atividade 01 - Entendimento do Flask

Atividade 02 - Criar os endpoint necessários para a interface de login

1 - Use fast API
2 - Definir @app.get("/home")  @app.get("/") @app.get("/login")
3 - Os dados devem ser listados de forma static


Atividade 03 - Criar Login da aplicação seloedu utilizando o flask-login

1 - Instalar e configurar o `flask-login`
2 - Criar o modelo de usuário
3 - Configurar o `LoginManager` e o `user_loader`
4 - Criar as rotas `/login`, `/logout` e `/home`
5 - Proteger a rota `/home` com `@login_required`
6 - Criar a tela de login e validar usuário e senha


Atividade 04 - Recuperação de senha da tela de login

Implementar o fluxo de recuperação de senha com envio de link por e-mail, simulando o SMTP local com Docker MailHog para testes sem envio real.
1 Configurar as chaves de e-mail em `config.py` (`MAIL_SERVER`, `MAIL_PORT`, `MAIL_DEFAULT_SENDER`).
2 Implementar as rotas `/esqueci-senha` e `/redefinir-senha` no `app.py`.
3 Criar as telas `templates/auth/forgot_password.html` e `templates/auth/reset_password.html`.
4 Validar o token e atualizar a senha do usuário.

OBS: o link de redefinição é gerado e exibido na interface (sem envio real por e-mail). A simulação com MailHog está preparada nas configurações e pode ser ativada ao integrar `Flask-Mail` no fluxo em execução.

Para simular envio de e-mail com Docker MailHog:

1 Subir o MailHog:
```bash
docker run --rm -p 1025:1025 -p 8025:8025 mailhog/mailhog
```

2 Acessar a caixa de entrada simulada:
`http://localhost:8025`

3 Executar o fluxo de recuperação em `/esqueci-senha` e verificar o e-mail no painel do MailHog.

Atividade 05 - Definição de relação de tabelas
