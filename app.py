from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        try:
            peso = float(request.form['peso'])
            hto = float(request.form['hto'])
            extraccion = float(request.form['extraccion'])
            C = float(request.form['ultrafiltrado'])
            Qd = float(request.form['dialisis'])
            FF = float(request.form['ff'])
            Repos = request.form['reposicion']

            if not (10 <= peso <= 190):
                raise ValueError("Peso fuera de rango (10-190 kg)")
            if not (1 <= hto <= 60):
                raise ValueError("Hematocrito fuera de rango (1-60%)")

            DC = C * peso
            Qp = (DC / FF) * 100 / 60
            Qs = Qp / ((100 - hto) / 100)
            D = Qd * peso
            o = Qp * 60

            if Repos == "Pre":
                Qr = ((100 * extraccion - FF * o) / (FF - 100))
                rep_texto = f"Reposición Prefiltro: {round(Qr)} ml/h"
            elif Repos == "Post":
                Qr = DC - extraccion
                rep_texto = f"Reposición Postfiltro: {round(Qr)} ml/h"
            elif Repos == "Mix":
                Qr1 = ((100 * (extraccion / 2) - FF * o) / (FF - 100)) / 2
                Qr = DC - extraccion / 2
                Qr2 = Qr - Qr1
                rep_texto = f"Reposición Mixta:<br>Prefiltro: {round(Qr1)} ml/h<br>Postfiltro: {round(Qr2)} ml/h"
            else:
                raise ValueError("Tipo de reposición inválido")

            resultado = {
                "reposicion": rep_texto,
                "flujo_sangre": f"{round(Qs)} ml/min",
                "dializante": f"{round(D)} ml/h",
                "extraccion": f"{extraccion} ml/h",
                "resumen": f"Peso: {peso} kg, Hto: {hto} %, FF: {FF} %, Diálisis: {Qd} ml/kg/h, Ultrafiltrado: {C} ml/kg/h"
            }

        except Exception as e:
            resultado = {"error": str(e)}

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
