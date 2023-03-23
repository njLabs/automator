def nearest_round(x, num=50):
    rounded_price = int(round(float(x) / num) * num)
    return rounded_price


def nearest_round_decimal(x, a):
    return round(round(x / a) * a, 2)