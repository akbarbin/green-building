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

def calculate_p33(raw_value):
  # New Antecedent/Consequent objects hold universe variables and membership
  # functions
  p33 = ctrl.Antecedent(create_range_list(0.0, 1.0, 0.1), 'Ozone Depletion Potential (P33)')
  decision_value1 = ctrl.Consequent(create_range_list(0.0, 1.0, 0.1), 'Decision Value for P33, P34, P33, P69 & P71')

  p33['Low'] = fuzz.trapmf(p33.universe, [0.0, 0.0, 0.2, 0.4])
  p33['Medium'] = fuzz.trapmf(p33.universe, [0.2, 0.4, 0.6, 0.8])
  p33['High'] = fuzz.trapmf(p33.universe, [0.6, 0.8, 1.0, 1.0])

  # Consequent 1
  decision_value1['Bronze'] = fuzz.trapmf(decision_value1.universe, [0.0, 0.0, 0.2, 0.4])
  decision_value1['Silver'] = fuzz.trapmf(decision_value1.universe, [0.2, 0.4, 0.6, 0.8])
  decision_value1['Gold'] = fuzz.trapmf(decision_value1.universe, [0.6, 0.8, 1.0, 1.0])

  rule1 = ctrl.Rule(p33['Low'], decision_value1['Gold'])
  rule2 = ctrl.Rule(p33['Medium'], decision_value1['Silver'])
  rule3 = ctrl.Rule(p33['High'], decision_value1['Bronze'])

  performancepoint_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
  performancepoint = ctrl.ControlSystemSimulation(performancepoint_ctrl)

  performancepoint.input['Ozone Depletion Potential (P33)'] = raw_value

  # Crunch the numbers
  performancepoint.compute()

  point = performancepoint.output['Decision Value for P33, P34, P33, P69 & P71']

  return point