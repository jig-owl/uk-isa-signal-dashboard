from fastapi import FastAPI, Query
from signal_engine import analyze_stock

app = FastAPI(title="UK ISA Signal API")

@app.get("/")
def root():
    return {"message": "UK ISA Signal Engine is running"}

@app.get("/analyze")
def analyze(
    ticker: str = Query(..., description="LSE ticker e.g. BP.L"),
    capital: float = Query(..., description="Capital in GBP")
):
    try:
        result = analyze_stock(ticker, capital)
        return result
    except Exception as e:
        return {"error": "Internal Server Error", "details": str(e)}
