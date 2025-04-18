// Zmiana wartości po zmianie waluty w polu #secondCurr
async function updateRate() {
    // Pobieranie danych z aplikacji
    const selectedCurrency = document.getElementById("secondCurrIndex").value;
    const selectedOption = document.querySelector('input[name="options"]:checked').id;

    const dataCurr = {
            currency: selectedCurrency,
            option: selectedOption,
        };

    // Przekazywanie danych do backendu
    try {
        const response = await fetch('/get_rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataCurr),
        });

        if (response.ok) {
            // Pobieranie danych z backendu
            const data = await response.json();

            // Jeśli wystąpił błąd, wyświetlamy komunikat
            if (data.error) {
                document.getElementById("secondCurr").innerHTML = `<p>${data.error}</p>`;
                return;
            }
            console.log("Otrzymane dane z backendu:", data);

            // Wyświetlenie kursu w polu
            val = Math.abs(document.getElementById("firstCurr").value);
            document.getElementById("firstCurr").value = val;
            document.getElementById("secondCurr").value = (val * data.rate).toFixed(2);

        } else {
            console.error("Błąd serwera:", response.statusText);
            document.getElementById("secondCurr").innerHTML = "<p>Nie udało się załadować danych waluty.</p>";
        }
    } catch (error) {
        console.error("Błąd podczas aktualizacji kursu:", error);
        document.getElementById("secondCurr").innerHTML = "<p>Nie udało się załadować kursu.</p>";
    }
}


// Zmiana wartości po zmianie wartości w polu #firstCurr, #secondCurr
async function updateRatePLN() {
    // Pobieranie danych z aplikacji
    const selectedCurrency = document.getElementById("secondCurrIndex").value;
    selectedCurrency = Math.abs(selectedCurrency);
    const selectedOption = document.querySelector('input[name="options"]:checked').id;

    const dataCurr = {
            currency: selectedCurrency,
            option: selectedOption,
        };

    // Przekazywanie danych do backendu
    try {
        const response = await fetch('/get_rate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataCurr),
        });

        if (response.ok) {
            // Pobieranie danych z backendu
            const data = await response.json();

            // Jeśli wystąpił błąd, wyświetlamy komunikat
            if (data.error) {
                document.getElementById("firstCurr").innerHTML = `<p>${data.error}</p>`;
                return;
            }
            console.log("Otrzymane dane z backendu:", data);

            // Wyświetlenie kursu w polu
            val = Math.abs(document.getElementById("secondCurr").value);
            document.getElementById("secondCurr").value = val;
            document.getElementById("firstCurr").value = (val * data.rate).toFixed(2);

        } else {
            console.error("Błąd serwera:", response.statusText);
            document.getElementById("firstCurr").innerHTML = "<p>Nie udało się załadować danych waluty.</p>";
        }
    } catch (error) {
        console.error("Błąd podczas aktualizacji kursu:", error);
        document.getElementById("firstCurr").innerHTML = "<p>Nie udało się załadować kursu.</p>";
    }
}



// Aktualizacja wykresu
async function updateChart() {

    // Pobieranie danych z aplikacji
    const selectedCurrency = document.getElementById("secondCurrIndex").value;
    const selectedOption = document.querySelector('input[name="options"]:checked').id;
    const rangeData = document.getElementById("dateRange").value;
    const selectedRange = document.querySelector('input[name="radio-range"]:checked').value;

    // Sprawdzanie typy zakresu
    if (selectedRange != 0) {
        $("#dateRange").attr("disabled", true);
    }
    else {
        $("#dateRange").attr("disabled", false);
    }

    const dataChart = {
        currency: selectedCurrency,
        option: selectedOption,
        rangeDate: rangeData,
        radioRange: selectedRange,
    };

    // Przekazywanie danych do backendu
    try {
        const response = await fetch('/get_chart', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dataChart),
        });


        if (response.ok) {
            const data = await response.json();
            // Jeśli wystąpił błąd, wyświetlamy komunikat
            if (data.error) {
                document.getElementById("chart-container").innerHTML = `<p>${data.error}</p>`;
                return;
            }
            console.log("Otrzymane dane z backendu:", data);
            // Renderowanie wykresu za pomocą Plotly.newPlot
            Plotly.newPlot('chart-container', data.fig_dict.data, data.fig_dict.layout, { displayModeBar: false });
            document.getElementById("dateRange").value = data.firstDate + " to " + data.secondDate;

        } else {
            console.error("Błąd serwera:", response.statusText);
            document.getElementById("chart-container").innerHTML = "<p>Nie udało się załadować danych wykresu.</p>";
        }
    } catch (error) {
        console.error("Błąd podczas aktualizacji wykresu:", error);
        document.getElementById("chart-container").innerHTML = "<p>Nie udało się załadować wykresu.</p>";
    }
}

// funkcja wykonująca dwie funkcje dla #secondCurr
async function updateChartAndRate() {
    updateChart();
    updateRate();
}

// funkcja wykonująca dwie funkcje dla #firstCurr
async function updateChartAndRatePLN() {
    updateChart();
    updateRatePLN();
}

// Generowanie kalendarza
document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#dateRange", {
        mode: "range",
        maxDate: "today",
        minDate: "2002-01-02",  // UWAGA: Format powinien pasować do `dateFormat`
        defaultDate: [dateRange.startDate, dateRange.endDate],
        dateFormat: "Y-m-d",    // Format "Rok-miesiac-dzien"
        onClose: function(selectedDates, dateStr, instance) {
            console.log("Zakres dat wybrany po zamknięciu:", dateStr);
            updateChart();  // Wywołanie funkcji aktualizacji po wyborze zakresu dat
        },
        onOpen: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 1) {
                instance.jumpToDate(selectedDates[1]); // Przeskocz do końcowej daty zakresu
            }
        }

    });
});



// Data w stopnce
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("year").innerHTML = new Date().getFullYear();
});


