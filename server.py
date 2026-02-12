import uvicorn as uv

if "__main__" == __name__:
    uv.run(app="app.main:app",host="127.0.0.1",port=8000,reload=True)