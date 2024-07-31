import uvicorn

if __name__ == "__main__":
    # run the test server, use nginx unit for actually running
    uvicorn.run(app="src.main:app", reload=True, workers=4)