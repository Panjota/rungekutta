def runge_kutta(f, x0, y0, h, num_steps):
    x_values = [x0]
    y_values = [y0]

    for _ in range(num_steps):
        k1 = h * f(x0, y0)
        k2 = h * f(x0 + h / 2, y0 + k1 / 2)
        k3 = h * f(x0 + h / 2, y0 + k2 / 2)
        k4 = h * f(x0 + h, y0 + k3)

        y_new = y0 + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        y0 = y_new
        x0 += h

        x_values.append(x0)
        y_values.append(y0)

    return x_values, y_values
