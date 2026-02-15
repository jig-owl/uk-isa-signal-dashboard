async function analyze() {

    const ticker = document.getElementById("ticker").value;
    const capital = document.getElementById("capital").value;
    const result = document.getElementById("result");

    const apiUrl = `https://uk-isa-signal-api.onrender.com/analyze?ticker=${ticker}&capital=${capital}`;

    result.innerHTML = "Loading...";

    try {
        const response = await fetch(apiUrl);
        const data = await response.json();

        if (data.error) {
            result.innerHTML = `<strong>Error:</strong> ${data.error}`;
            return;
        }

        result.innerHTML = `
            <strong>Signal:</strong> ${data.signal} <br>
            <strong>Reason:</strong> ${data.reason} <br>
            <strong>Trend:</strong> ${data.trend} <br>
            <strong>Price:</strong> £${data.price} <br>
            <strong>RSI:</strong> ${data.rsi} <br>
            <strong>Position Size:</strong> £${data.position_size} <br>
            <strong>Stop Price:</strong> £${data.stop_price}
        `;
    } catch (error) {
        result.innerHTML = "Network error.";
    }
}
