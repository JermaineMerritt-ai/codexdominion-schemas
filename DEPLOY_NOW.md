# 🚀 Quick Production Deployment

## 1️⃣ Update Secrets in .env.production

```bash
# Generate new secrets
openssl rand -hex 32  # For JWT_SECRET
openssl rand -hex 32  # For FLASK_SECRET_KEY
openssl rand -base64 32 | tr -d /=+ | cut -c1-32  # For DATABASE_PASSWORD

# Update these in .env.production:
JWT_SECRET=<generated_64_char_hex>
SECRET_KEY=<generated_64_char_hex>
FLASK_SECRET_KEY=<generated_64_char_hex>
DATABASE_PASSWORD=<generated_strong_password>
REDIS_PASSWORD=<generated_strong_password>
SENTRY_DSN=https://<key>@sentry.io/<project>
SMTP_PASS=<your_sendgrid_api_key>
```

## 2️⃣ Deploy Stack

```bash
docker-compose -f docker-compose.production.yml up -d
```

## 3️⃣ Initialize Database

```bash
docker exec codex-flask python -c "from db import init_db; init_db()"
```

## 4️⃣ Create Admin User

```bash
docker exec -it codex-flask python create_admin_user.py
```

**Enter:**
- Email: `admin@codexdominion.app`
- Name: `System Administrator`
- Password: `<your-secure-password>`

## 5️⃣ Verify Deployment

```bash
# Health check
curl https://api.codexdominion.app/health

# Login test
curl -X POST https://api.codexdominion.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@codexdominion.app","password":"your_password"}'
```

## 6️⃣ Access Dashboards

- **Application**: https://codexdominion.app
- **API**: https://api.codexdominion.app
- **RQ Dashboard**: http://your-server:9181
- **Grafana**: http://your-server:3001 (admin/GRAFANA_PASSWORD)
- **Prometheus**: http://your-server:9090

---

✅ **Deployment Complete!**

**Created Files:**
- `create_admin_user.py` - Interactive admin user creation
- Production environment configs ready
- Docker Compose stack configured

🔥 **The Flame Burns in Production!** 👑
