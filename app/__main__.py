import typer
import uvicorn

def main(host: bool = False):
    if host:
        uvicorn.run("app:app", host="0.0.0.0", port=80)
    else:
        uvicorn.run("app:app", reload=True)

if __name__ == "__main__":
    typer.run(main)