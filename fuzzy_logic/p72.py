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

def calculate_p72(raw_value):
  # New Antecedent/Consequent objects hold universe variables and membership
  # functions
  p72 = ctrl.Antecedent(create_range_list(-47, 74, 1), 'Temperature (P72)')
  decision_value2 = ctrl.Consequent(create_range_list(0.0, 1.1, 0.1), 'Decision Value for P72 & P73')

  p72['Cool'] = fuzz.trapmf(p72.universe, [-47, -47, -23, 1])
  p72['Comfortable'] = fuzz.trapmf(p72.universe, [-23, 1, 25, 49])
  p72['Hot'] = fuzz.trapmf(p72.universe, [25, 49, 73, 73])

  # Consequent 1
  decision_value2['Bad'] = fuzz.trapmf(decision_value2.universe, [0.0, 0.0, 0.2, 0.8])
  decision_value2['Good'] = fuzz.trapmf(decision_value2.universe, [0.2, 0.8, 1.0, 1.0])

  rule1 = ctrl.Rule(p72['Cool'] & p72['Hot'], decision_value2['Bad'])
  rule2 = ctrl.Rule(p72['Comfortable'], decision_value2['Good'])

  performancepoint_ctrl = ctrl.ControlSystem([rule1, rule2])
  performancepoint = ctrl.ControlSystemSimulation(performancepoint_ctrl)

  performancepoint.input['Temperature (P72)'] = raw_value

  # Crunch the numbers
  performancepoint.compute()

  point = performancepoint.output['Decision Value for P72 & P73']

  return point