import uvicorn 

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware import Middleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.connection import get_db, db_dependency
from src.config import settings
from src.routes import auth


app = FastAPI(debug=True)

app.include_router(auth.router, prefix='/api')


@app.get("/")
async def read_root():
    return {'Message': 'Hello World'}


@app.get(settings.HEALTH_CHECK_URL)
def healthchecker(db: db_dependency):

    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")


async def main():
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())