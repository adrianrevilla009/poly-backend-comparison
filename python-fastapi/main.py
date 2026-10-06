from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "UP"}


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    if order_id < 0:
        raise HTTPException(status_code=400, detail="bad id")
    return {"id": order_id, "customer": f"c-{order_id % 100}", "total": order_id % 1000 + 0.5, "status": "NEW"}
