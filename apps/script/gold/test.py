from gold_payments import KpiCalculator
import pandas as pd
calculator = KpiCalculator('data/cleaned_payments.csv')
result = calculator.best_payment_method()
print(result)