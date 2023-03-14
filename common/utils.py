def nearest_round(x, num=50):
    rounded_price = int(round(float(x) / num) * num)
    return rounded_price

