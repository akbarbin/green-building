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

def calculate_p63(raw_value):
  # New Antecedent/Consequent objects hold universe variables and membership
  # functions
  p63 = ctrl.Antecedent(create_range_list(0.0, 0.51, 0.01), 'Energy Increasing Percentage (P63)')
  decision_value1 = ctrl.Consequent(create_range_list(0.0, 1.1, 0.1), 'Decision Value for P33, P34, P63, P69 & P71')

  p63['Good'] = fuzz.trapmf(p63.universe, [0, 0, 0.1, 0.2])
  p63['Medium'] = fuzz.trapmf(p63.universe, [0.1, 0.2, 0.3, 0.4])
  p63['Bad'] = fuzz.trapmf(p63.universe, [0.3, 0.4, 0.5, 0.5])

  # Consequent 1
  decision_value1['Bronze'] = fuzz.trapmf(decision_value1.universe, [0.0, 0.0, 0.2, 0.4])
  decision_value1['Silver'] = fuzz.trapmf(decision_value1.universe, [0.2, 0.4, 0.6, 0.8])
  decision_value1['Gold'] = fuzz.trapmf(decision_value1.universe, [0.6, 0.8, 1.0, 1.0])

  rule1 = ctrl.Rule(p63['Bad'], decision_value1['Bronze'])
  rule2 = ctrl.Rule(p63['Medium'], decision_value1['Silver'])
  rule3 = ctrl.Rule(p63['Good'], decision_value1['Gold'])

  performancepoint_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
  performancepoint = ctrl.ControlSystemSimulation(performancepoint_ctrl)

  performancepoint.input['Energy Increasing Percentage (P63)'] = raw_value

  # Crunch the numbers
  performancepoint.compute()

  point = performancepoint.output['Decision Value for P33, P34, P63, P69 & P71']

  return point