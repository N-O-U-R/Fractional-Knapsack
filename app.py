from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

# Fractional Knapsack Algorithm for Multiple Vehicles
def fractional_knapsack_multi_vehicle(value, weight, capacities):
    index = list(range(len(value)))
    ratio = [v/w for v, w in zip(value, weight)]
    index.sort(key=lambda i: ratio[i], reverse=True)

    vehicle_loads = []
    for capacity in capacities:
        max_profit = 0
        fractions = [0] * len(value)
        for i in index:
            if weight[i] <= capacity:
                fractions[i] = 1
                max_profit += value[i]
                capacity -= weight[i]
            else:
                fractions[i] = capacity / weight[i]
                max_profit += value[i] * (capacity / weight[i])
                break
        vehicle_loads.append((max_profit, fractions))

    return vehicle_loads

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        num_vehicles = int(request.form['num_vehicles'])
        num_goods = int(request.form['num_goods'])
        return render_template('input_form.html', num_vehicles=num_vehicles, num_goods=num_goods)
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    num_vehicles = int(request.form['num_vehicles'])
    num_goods = int(request.form['num_goods'])
    values = [float(request.form[f'value_{i}']) for i in range(num_goods)]
    weights = [float(request.form[f'weight_{i}']) for i in range(num_goods)]
    capacities = [float(request.form[f'capacity_{i}']) for i in range(num_vehicles)]

    raw_result = fractional_knapsack_multi_vehicle(values, weights, capacities)
    result = [(round(profit, 4), [round(frac, 4) for frac in fractions]) for profit, fractions in raw_result]

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
