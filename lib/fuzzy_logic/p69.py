import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def calculate_p69(raw_value):
  # New Antecedent/Consequent objects hold universe variables and membership
  # functions
  p69 = ctrl.Antecedent(np.arange(0.0, 0.51, 0.01), 'Water Increasing Percentage (P69)')
  decision_value1 = ctrl.Consequent(np.arange(0.0, 1.1, 0.1), 'Decision Value for P33, P34, P63, P69 & P71')

  p69['Good'] = fuzz.trapmf(p69.universe, [0.0, 0.0, 0.1, 0.2])
  p69['Medium'] = fuzz.trapmf(p69.universe, [0.1, 0.2, 0.3, 0.4])
  p69['Bad'] = fuzz.trapmf(p69.universe, [0.3, 0.4, 0.5, 0.5])

  # Consequent 1
  decision_value1['Bronze'] = fuzz.trapmf(decision_value1.universe, [0.0, 0.0, 0.2, 0.4])
  decision_value1['Silver'] = fuzz.trapmf(decision_value1.universe, [0.2, 0.4, 0.6, 0.8])
  decision_value1['Gold'] = fuzz.trapmf(decision_value1.universe, [0.6, 0.8, 1.0, 1.0])

  rule1 = ctrl.Rule(p69['Bad'], decision_value1['Bronze'])
  rule2 = ctrl.Rule(p69['Medium'], decision_value1['Silver'])
  rule3 = ctrl.Rule(p69['Good'], decision_value1['Gold'])

  performancepoint_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
  performancepoint = ctrl.ControlSystemSimulation(performancepoint_ctrl)

  performancepoint.input['Water Increasing Percentage (P69)'] = raw_value

  # Crunch the numbers
  performancepoint.compute()

  point = performancepoint.output['Decision Value for P33, P34, P63, P69 & P71']

  return point