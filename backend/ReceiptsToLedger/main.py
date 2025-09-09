from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from ReceiptsToLedger.api import auth, transactions, matches, journal, users
from ReceiptsToLedger.core.db import Base, engine
from ReceiptsToLedger.core.ratelimit import limiter

app = FastAPI(title="Receipts-to-Ledger")



# DB init
Base.metadata.create_all(bind=engine)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

# Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
app.include_router(matches.router, prefix="/matches", tags=["matches"])
app.include_router(journal.router, prefix="/journal", tags=["journal"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

# Custom Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description="Receipts-to-Ledger API Docs",
        routes=app.routes,
    )

    # 👇 Add global BearerAuth scheme
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # 👇 Apply BearerAuth as default to every path
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
