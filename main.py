import uvicorn

if __name__ == "__main__":
    uvicorn.run("App:biblioteca",
                host="0.0.0.0",
                port=8000,
                reload=False,
                ssl_keyfile = "key.pem",
                ssl_certfile = "cert.pem",
                )
