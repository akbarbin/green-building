import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def calculate_p71(raw_value):
  # New Antecedent/Consequent objects hold universe variables and membership
  # functions
  p71 = ctrl.Antecedent(np.arange(0, 31, 1), 'Max Water Lab Month (P71)')
  decision_value1 = ctrl.Consequent(np.arange(0.0, 1.1, 0.1), 'Decision Value for P33, P34, P33, P69 & P71')

  p71['New'] = fuzz.trapmf(p71.universe, [0, 0, 6, 12])
  p71['Moderate'] = fuzz.trapmf(p71.universe, [6, 12, 18, 24])
  p71['Long'] = fuzz.trapmf(p71.universe, [18, 24, 30, 30])

  # Consequent 1
  decision_value1['Bronze'] = fuzz.trapmf(decision_value1.universe, [0.0, 0.0, 0.2, 0.4])
  decision_value1['Silver'] = fuzz.trapmf(decision_value1.universe, [0.2, 0.4, 0.6, 0.8])
  decision_value1['Gold'] = fuzz.trapmf(decision_value1.universe, [0.6, 0.8, 1.0, 1.0])

  rule1 = ctrl.Rule(p71['New'], decision_value1['Gold'])
  rule2 = ctrl.Rule(p71['Moderate'], decision_value1['Silver'])
  rule3 = ctrl.Rule(p71['Long'], decision_value1['Bronze'])

  performancepoint_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
  performancepoint = ctrl.ControlSystemSimulation(performancepoint_ctrl)

  performancepoint.input['Max Water Lab Month (P71)'] = raw_value

  # Crunch the numbers
  performancepoint.compute()

  point = performancepoint.output['Decision Value for P33, P34, P33, P69 & P71']

  return point