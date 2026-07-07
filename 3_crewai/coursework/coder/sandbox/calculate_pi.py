def calculate_series(n):
    total = 0.0
    for i in range(n):
        # The series is 1/1 - 1/3 + 1/5 - 1/7 + ...
        # Term i (starting from 0) is (-1)^i / (2*i + 1)
        term = (1.0 / (2 * i + 1)) if i % 2 == 0 else (-1.0 / (2 * i + 1))
        total += term
    return total * 4

n = 1000000
result = calculate_series(n)
print(result)
