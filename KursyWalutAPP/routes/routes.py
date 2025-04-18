from KursyWalutAPP.routes import routes_bp
from KursyWalutAPP.forms import Form
from KursyWalutAPP.utils import currRate, currRateMid, chartData, convertDayWeek, stringToDT, dtToString
import datetime as dt


import json
from flask import render_template, request, jsonify


@routes_bp.route('/', methods=['GET', 'POST'])
def index():
    endDate = dt.datetime.today()
    startDate = endDate - dt.timedelta(days=90)
    dates = {
        "startDate": convertDayWeek(startDate),
        "endDate": convertDayWeek(endDate)
    }
    form = Form()
    fig = chartData("eur", "mid", convertDayWeek(startDate), convertDayWeek(endDate))
    plot_html = fig.to_html(config={'displayModeBar': False}, full_html=False)
    return render_template("index.html", form=form, plot_html=plot_html, dates=dates)

@routes_bp.route('/get_rate', methods=['POST'])
def get_rate():
    try:
        data = request.json  # Pobranie danych z zapytania (np. waluty)
        selected_currency = data.get("currency")
        if data.get("option") == "mid":
            rate = currRateMid(selected_currency[0:3])  # Pobranie kursu
            return jsonify({"rate": round(rate, 2)})  # Zwrot kursu w formacie JSON
        else:
            rate = currRate(selected_currency[0:3])  # Pobranie kursu
            print(rate)
            return jsonify({"rate": round(rate[data.get("option")], 2)})  # Zwrot kursu w formacie JSON
    except Exception as e:
        print(f"Błąd serwera przy pobieraniu kursu wakuty {selected_currency[0:3]}: {e}")  # Wyświetlanie szczegółów błędu w konsoli serwera
        return jsonify({'error': '<p>Błąd serwera: Nie udało pobrać danych z API.</p>'}), 500

@routes_bp.route('/get_chart', methods=['POST'])
def get_chart():
    try:
        data = request.json  # Pobranie danych z zapytania
        index = data.get("currency")[0:3]  # Pobieranie indeksu waluty
        typeCurr = data.get("option")  # Pobieranie rodzaju kursu
        if data.get("radioRange") == "max":
            radioRange = abs((dt.date.today() - dt.date(2002, 1, 2)).days)
        else:
            radioRange = int(data.get("radioRange"))
        range = data.get("rangeDate")  # Pobieranie zakresu dat
        firstDate, secondDate = range.split(" to ")  # Rozdzielanie dat
        if radioRange:  # Jeżeli != 0
            secondDate = dt.datetime.today()
            firstDate = dtToString(secondDate - dt.timedelta(days=radioRange))
            secondDate = dtToString(secondDate)
        print(f"Debug backend: {index}, {typeCurr}, {firstDate}, {secondDate}")  # Debug w konsoli serwera
        fig = chartData(index, typeCurr, firstDate, secondDate)
        fig_json = fig.to_json()
        fig_dict = json.loads(fig_json)  # Konwertuje string na słownik
        return jsonify({'fig_dict': fig_dict, 'firstDate': firstDate, 'secondDate': secondDate})

    except Exception as e:
        print(f"Błąd serwera przy generowaniu wykresu: {e}")  # Wyświetlanie szczegółów błędu w konsoli serwera
        return jsonify({'error': '<p>Błąd serwera: Nie udało się wygenerować wykresu.</p>'}), 500