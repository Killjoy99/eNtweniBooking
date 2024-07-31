import uvicorn

if __name__ == "__main__":
    # run the test server, use nginx unit for actually running
    uvicorn.run(app="src.main:app", host="0.0.0.0", port=8000, reload=True, workers=4)