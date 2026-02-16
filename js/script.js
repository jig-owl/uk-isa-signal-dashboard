document.getElementById("analyze-btn").addEventListener("click", async () => {
    const ticker = document.getElementById("ticker").value.trim();
    const capital = document.getElementById("capital").value;

    if (!ticker || !capital) {
        alert("Please enter both ticker and capital");
        return;
    }

    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "Loading...";

    try {
        const response = await fetch(`https://uk-isa-signal-system.onrender.com/analyze?ticker=${ticker}&capital=${capital}`);
        const data = await response.json();

        if (data.error) {
            resultDiv.innerHTML = `<span style="color:red">${data.error}</span>`;
        } else {
            resultDiv.innerHTML = `
                <strong>Ticker:</strong> ${data.ticker}<br>
                <strong>Signal:</strong> ${data.signal}<br>
                <strong>Reason:</strong> ${data.reason}<br>
                <strong>Price:</strong> ${data.price}<br>
                <strong>Trend:</strong> ${data.trend}<br>
                <strong>RSI:</strong> ${data.rsi}<br>
                <strong>Position Size:</strong> ${data.position_size}<br>
                <strong>Risk per Trade:</strong> ${data.risk_per_trade}<br>
                <strong>Stop Price:</strong> ${data.stop_price}<br>
            `;
        }
    } catch (err) {
        resultDiv.innerHTML = `<span style="color:red">Error fetching data</span>`;
        console.error(err);
    }
});
