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

def calculate_p73(raw_value):
  # New Antecedent/Consequent objects hold universe variables and membership
  # functions
  p73 = ctrl.Antecedent(create_range_list(-90, 161, 1), 'Humidity (P73)')
  decision_value2 = ctrl.Consequent(create_range_list(0.0, 1.1, 0.1), 'Decision Value for P72 & P73')

  p73['Dry'] = fuzz.trapmf(p73.universe, [-90, -90, -40, 10])
  p73['Comfortable'] = fuzz.trapmf(p73.universe, [-40, 10, 60, 110])
  p73['Overcast'] = fuzz.trapmf(p73.universe, [60, 110, 160, 160])

  # Consequent 1
  decision_value2['Bad'] = fuzz.trapmf(decision_value2.universe, [0.0, 0.0, 0.2, 0.8])
  decision_value2['Good'] = fuzz.trapmf(decision_value2.universe, [0.2, 0.8, 1.0, 1.0])

  rule1 = ctrl.Rule(p73['Dry'] & p73['Overcast'], decision_value2['Bad'])
  rule2 = ctrl.Rule(p73['Comfortable'], decision_value2['Good'])

  performancepoint_ctrl = ctrl.ControlSystem([rule1, rule2])
  performancepoint = ctrl.ControlSystemSimulation(performancepoint_ctrl)

  performancepoint.input['Humidity (P73)'] = raw_value

  # Crunch the numbers
  performancepoint.compute()

  point = performancepoint.output['Decision Value for P72 & P73']

  return point