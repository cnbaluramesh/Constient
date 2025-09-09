# 📘 Project: Receipts-to-Ledger Mini App

## 1. Setup & Run Instructions

### Local Development
```bash
# Clone repo
git clone https://github.com/cnbaluramesh/Constient.git
cd Constien

# Setup Python/Node environment
python -m venv venv && source venv/bin/activate   # if Python backend
npm install                                       # if frontend
```

### Docker / Docker Compose
```bash
# Build and start services
docker-compose up --build

# Run migrations
docker-compose exec backend alembic upgrade head   # (if using Alembic/SQLAlchemy)
docker-compose exec backend npm run migrate        # (if using Prisma/Sequelize)
```

### Environment Variables
Copy and fill in `.env.example`:
```bash
cp .env.example .env
```

---

## 2. Sample Users

| Role   | Email                | Password      |
|--------|----------------------|---------------|
| Admin  | admin@orga.com    | password      |
| Analyst| analyst@orga.com  | password      |

---

## 3. Design Decisions & Trade-offs

*(½–1 page of prose; replace bullets with your own notes)*

- **Framework choice**: (e.g., FastAPI + Postgres for speed & strong typing).  
- **Trade-offs**: (e.g., skipped async file storage to focus on ingest logic).  
- **Assumptions**: (e.g., one currency per invoice; no multi-tenant UI).  
- **Performance considerations**: (e.g., added indexes on `invoice_no`, `tenant_id`).  

---

## 4. API Overview

### Auth - Admin
```bash
curl -X POST http://localhost:8000/api/login   -H "Content-Type: application/json"   -d '{"email":"admin@orga.com","password":"password"}'
```

Response:
```json
{ "access_token": "<jwt>", "role": "admin" }
```


### Auth - Analyst
```bash
curl -X POST http://localhost:8000/api/login   -H "Content-Type: application/json"   -d '{"email":"analyst@orga.com","password":"password"}'
```

Response:
```json
{ "access_token": "<jwt>", "role": "analyst" }
```

### Upload CSV
```bash
curl -X POST http://localhost:8000/api/upload   -H "Authorization: Bearer <jwt>"   -F "file=@sample.csv"
```

### Match Preview
```bash
curl http://localhost:8000/api/matches?batch_id=123   -H "Authorization: Bearer <jwt>"
```

### Journal Preview
```bash
curl http://localhost:8000/api/journal/123   -H "Authorization: Bearer <jwt>"
```

---

## 5. Known Limitations

- Example: *No pagination on invoices — large datasets may be slow.*   - Implemented
- Example: *RBAC not fully enforced in frontend yet.*  - Implemented
- Example: *CSV ingest does not support multi-currency rows.*  - Implemented

---

## 6. Demo

Choose **one**:  

### Option A: Video
- [Loom Link] https://www.loom.com/share/576b98d470244472882c37f518649fd8?sid=e13f23ac-2209-4b46-9b47-dce19376a84f  showing login → upload → review → journal preview.  

### Option B: Markdown Script
*(put in `DEMO.md`)*  
```markdown
1. Login as admin@example.com
2. Upload `sample.csv` (provided in repo)
3. Go to Matches table → verify confidence scores
4. Navigate to Journal Preview → confirm balanced DR/CR entries
```
## 7. NextJs Template reference Link: 

https://github.com/Kiranism/next-shadcn-dashboard-starter 

removed : Auth - Clerk 


## 8. Run seed inside Docker container

If your backend runs inside Docker (receipts-to-ledger-backend only one time execution of below command):

docker exec -it receipts-to-ledger-backend python seed.py

## 9. Run Locally
1. `cp .env.example .env`
2. `docker-compose up --build`
3. Open http://localhost:3001 for frontend
4. API runs on http://localhost:8000