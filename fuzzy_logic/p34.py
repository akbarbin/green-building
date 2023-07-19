import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def create_range_list(start, end, step):
    arr = []
    current_value = start

    while current_value <= end:
        arr.append(current_value)
        current_value += step

    return arr

def calculate_p34(raw_value):
  # New Antecedent/Consequent objects hold universe variables and membership
  # functions
  p34 = ctrl.Antecedent(create_range_list(0, 3501, 35), 'Global Warming Potential (P34)')
  decision_value1 = ctrl.Consequent(create_range_list(0.0, 1.1, 0.1), 'Decision Value for P33, P34, P33, P69 & P71')

  p34['Low'] = fuzz.trapmf(p34.universe, [0, 0, 700, 1400])
  p34['Medium'] = fuzz.trapmf(p34.universe, [700, 1400, 2100, 2800])
  p34['High'] = fuzz.trapmf(p34.universe, [2100, 2800, 3500, 3500])

  # Consequent 1
  decision_value1['Bronze'] = fuzz.trapmf(decision_value1.universe, [0.0, 0.0, 0.2, 0.4])
  decision_value1['Silver'] = fuzz.trapmf(decision_value1.universe, [0.2, 0.4, 0.6, 0.8])
  decision_value1['Gold'] = fuzz.trapmf(decision_value1.universe, [0.6, 0.8, 1.0, 1.0])

  rule1 = ctrl.Rule(p34['Low'], decision_value1['Gold'])
  rule2 = ctrl.Rule(p34['Medium'], decision_value1['Silver'])
  rule3 = ctrl.Rule(p34['High'], decision_value1['Bronze'])

  performancepoint_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
  performancepoint = ctrl.ControlSystemSimulation(performancepoint_ctrl)

  performancepoint.input['Global Warming Potential (P34)'] = raw_value

  # Crunch the numbers
  performancepoint.compute()

  point = performancepoint.output['Decision Value for P33, P34, P33, P69 & P71']

  return point