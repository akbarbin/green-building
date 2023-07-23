from flask import Flask, request, render_template, redirect, url_for
from fuzzy_logic.p33 import calculate_p33
from fuzzy_logic.p34 import calculate_p34
from fuzzy_logic.p63 import calculate_p63
from fuzzy_logic.p69 import calculate_p69
from fuzzy_logic.p71 import calculate_p71
from fuzzy_logic.p72 import calculate_p72
from fuzzy_logic.p73 import calculate_p73
from datetime import datetime
import json
import math
import os

app = Flask(__name__)
my_dir = os.path.dirname(__file__)

@app.route('/')
def index():
  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      buildings = json.load(file)
  except FileNotFoundError:
    buildings = []

  return render_template('index.html', buildings=buildings)

@app.route('/buildings/new')
def new():
  # Adding default value in the new form
  data = '{"name": "", "p01": "No", "p02": "No", "p03": "No", "p04": "No", "p05": "No", "p06": "No", "p07": "No", "p08": "No", "p09": "No", "p10": "No", "p11": "No", "p12": "No", "p13": "No", "p14": "No", "p15": "No", "p16": "No", "p17": "No", "p18": "No", "p19": "No", "p20": "No", "p21": "No", "p22": "No", "p23": "No", "p24": "No", "p25": "No", "p26": "No", "p27": "No", "p28": "No", "p29": "No", "p30": "No", "p31": "No", "p32": "No", "p33": 0, "p34": 675, "p35": "No", "p36": "No", "p37": "No", "p38": "No", "p39": "No", "p40": "No", "p41": "No", "p42": "No", "p43": "No", "p44": "No", "p45": "No", "p46": "No", "p47": "No", "p48": "No", "p49": "No", "p50": "No", "p51_1": 3000, "p51_2": 4000, "p51_3": 5000, "p51_4": 4000, "p51_5": 7000, "p51_6": 1500, "p52": "No", "p53": "No", "p54": "No", "p55": "No", "p56": "No", "p57": "No", "p58": "No", "p59": "No", "p60": "No", "p61_1": 4000000.0, "p61_2": 5000000.0, "p61_3": 4000000.0, "p61_4": 4000000.0, "p61_5": 5000000.0, "p61_6": 4400000.0, "p62": "No", "p63": 500000000, "p64": "No", "p65": "No", "p66": "No", "p67_1": 5.0, "p67_2": 5.0, "p68_1": 4000000,  "p68_2": 4000000, "p68_3": 4000000, "p68_4": 4000000, "p68_5": 4000000, "p68_6": 4200000, "p69": 10000000, "p70": "No", "p71": "2022/12/09", "p72": 23.0, "p73": 36, "p74": "No", "p75": "No", "p76": "No", "p77": "No", "p78": "No", "p79_1": 33.48, "p79_2": 32.40, "p79_3": 34.56, "p79_4": 29.64, "p79_5": 16.44, "p79_6": 35.76,  "p80": "No", "p81": "No", "p82": "No", "p83": "No"}'
  building = json.loads(data)
  return render_template('new.html', building=building)

@app.route('/buildings', methods=['POST'])
def create():
  form_data = request.form.to_dict()

  # Reading JSON file
  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      json_data = json.load(file)
  except FileNotFoundError:
    json_data = []

  # Changing string data type into correct one
  form_data['id'] = json_data[-1].get('id', 0) + 1 if len(json_data) else 1
  form_data['p33'] = float(form_data['p33'])
  form_data['p34'] = int(form_data['p34'])
  form_data['p63'] = float(form_data['p63'])
  form_data['p69'] = float(form_data['p69'])
  form_data['p51_1'] = float(form_data['p51_1'])
  form_data['p51_2'] = float(form_data['p51_2'])
  form_data['p51_3'] = float(form_data['p51_3'])
  form_data['p51_4'] = float(form_data['p51_4'])
  form_data['p51_5'] = float(form_data['p51_5'])
  form_data['p51_6'] = float(form_data['p51_6'])
  form_data['p61_1'] = float(form_data['p61_1'])
  form_data['p61_2'] = float(form_data['p61_2'])
  form_data['p61_3'] = float(form_data['p61_3'])
  form_data['p61_4'] = float(form_data['p61_4'])
  form_data['p61_5'] = float(form_data['p61_5'])
  form_data['p61_6'] = float(form_data['p61_6'])
  form_data['p67_1'] = float(form_data['p67_1'])
  form_data['p67_2'] = float(form_data['p67_2'])
  form_data['p68_1'] = float(form_data['p68_1'])
  form_data['p68_2'] = float(form_data['p68_2'])
  form_data['p68_3'] = float(form_data['p68_3'])
  form_data['p68_4'] = float(form_data['p68_4'])
  form_data['p68_5'] = float(form_data['p68_5'])
  form_data['p68_6'] = float(form_data['p68_6'])
  form_data['p79_1'] = float(form_data['p79_1'])
  form_data['p79_2'] = float(form_data['p79_2'])
  form_data['p79_3'] = float(form_data['p79_3'])
  form_data['p79_4'] = float(form_data['p79_4'])
  form_data['p79_5'] = float(form_data['p79_5'])
  form_data['p79_6'] = float(form_data['p79_6'])
  form_data['p72'] = float(form_data['p72'])
  form_data['p73'] = float(form_data['p73'])

  # pre-processing
  form_data['p63'] = (form_data['p61_6'] - form_data['p63']) / form_data['p63']
  form_data['p69'] = (form_data['p68_6'] - form_data['p69']) / form_data['p69']
  start = datetime.strptime(form_data['p71'], "%Y-%m-%d")
  end = datetime.now()
  res = (end.year - start.year) * 12 + (end.month - start.month)
  form_data['p71'] = res

  # Adding form_data to json_data array
  json_data.append(form_data)

  # Saving array json_data into JSON file
  filename = os.path.join(my_dir, 'data/buildings.json')
  os.makedirs(os.path.dirname(filename), exist_ok=True)

  with open(filename, 'w') as file:
    json.dump(json_data, file, indent=2, separators=(',', ': '))
    file.write('\n')  # Adding new line

  return redirect(url_for('show', id= form_data['id']))

@app.route('/buildings/<int:id>')
def show(id):
  # Reading JSON file
  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      buildings = json.load(file)
  except FileNotFoundError:
    buildings = []

  building = find_json_by('id', buildings, id)

  return render_template('show.html', building=building)

@app.route('/buildings/<int:id>/evaluate', methods=['POST'])
def evaluate(id):
  # Reading JSON file
  try:
    filename = os.path.join(my_dir, 'parameters.json')

    with open(filename, 'r') as file:
      parameters_json_data = json.load(file)
  except FileNotFoundError:
    parameters_json_data = []

  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      buildings_json_data = json.load(file)
  except FileNotFoundError:
    buildings_json_data = []

  # ax
  ax_params = []
  for sub in parameters_json_data:
    if sub['group'] == 'ax':
      ax_params.append(sub)

  assessments = []
  for building in buildings_json_data:
    total_ax = 0
    for ax_param in ax_params:
      # encoding
      if building[ax_param['code']] == 'Yes':
        point = 1
      else:
        point = 0

      value = point * ax_param['weight']

      # Saving performance
      assessments.append({ "building_id": building['id'], "code": ax_param['code'], "point": point, "weight": ax_param['weight'], "value": value })

      total_ax += value

    # Saving ax into building
    building['ax'] = round(total_ax, 4)

  # bx
  bx_params = []
  for sub in parameters_json_data:
    if sub['group'] == 'bx':
      bx_params.append(sub)

  for building in buildings_json_data:
    total_bx = 0
    for bx_param in bx_params:
      if bx_param['code'] == 'p33':
        point = calculate_p33(building[bx_param['code']])

      if bx_param['code'] == 'p34':
        point = calculate_p34(building[bx_param['code']])

      if bx_param['code'] == 'p63':
        point = calculate_p63(building[bx_param['code']])

      if bx_param['code'] == 'p69':
        point = calculate_p69(building[bx_param['code']])

      if bx_param['code'] == 'p71':
        point = calculate_p71(building[bx_param['code']])

      if bx_param['code'] == 'p72':
        point = calculate_p72(building[bx_param['code']])

      if bx_param['code'] == 'p73':
        point = calculate_p73(building[bx_param['code']])

      value = round(point * bx_param['weight'], 4)

      # Saving performance
      assessments.append({ "building_id": building['id'], "code": bx_param['code'], "point": point, "weight": bx_param['weight'], "value": value })

      total_bx += value

    # Saving bx into building
    building['bx'] = round(total_bx, 4)

  # cx
  cx_params = []
  for sub in parameters_json_data:
    if sub['group'] == 'cx':
      cx_params.append(sub)

  slopes = []
  for building in buildings_json_data:
    value = 0
    for cx_param in cx_params:
      values = []
      months = [1, 2, 3, 4, 5, 6]

      for month in months:
        values.append(building[f"{cx_param['code']}_{month}"])

      slope = calculate_slope(values)
      slope = 0.1 if slope == 0.0 else slope
      slope = slope + abs(slope) + 0.01 if slope < 0.0 else slope

      slopes.append({ "building_id": building['id'], "code": cx_param['code'], "value": slope })

  min_slopes = []
  for cx_param in cx_params:
    collected_slopes = []
    for slope in slopes:
      if slope['code'] == cx_param['code']:
        collected_slopes.append(slope['value'])
    min_slopes.append({ "code": cx_param['code'], "value": min(collected_slopes) })

  points = []
  for slope in slopes:
    min_slope = find_json_by('code', min_slopes, slope['code'])
    point = min_slope['value'] / slope['value']
    points.append({ "building_id": slope['building_id'], "code": slope['code'], "value": point })

  for building in buildings_json_data:
    total_cx = 0
    for cx_param in cx_params:
      point = find_json_by_two_conditions(['code', 'building_id'], points, [cx_param['code'], building['id']])
      value = round(point['value'] * cx_param['weight'], 4)

      # Saving performance
      assessments.append({ "building_id": building['id'], "code": cx_param['code'], "point": point['value'], "weight": cx_param['weight'], "value": value })

      total_cx += value

    # Saving bx into building
    building['cx'] = round(total_cx, 4)

  # dx
  dx_params = []
  for sub in parameters_json_data:
    if sub['group'] == 'dx':
      dx_params.append(sub)

  distances = []
  for building in buildings_json_data:
    value = 0
    for dx_param in dx_params:
      reference = building[f"{dx_param['code']}_1"]
      reality = building[f"{dx_param['code']}_2"]
      reference = reference + (0.05 * reference) if reference == reality else reference
      distance = math.dist([reference], [reality])

      distances.append({ "building_id": building['id'], "code": dx_param['code'], "value": distance })

  min_distances = []
  for dx_param in dx_params:
    collected_distances = []
    for distance in distances:
      if distance['code'] == dx_param['code']:
        collected_distances.append(distance['value'])
    min_distances.append({ "code": dx_param['code'], "value": min(collected_distances) })

  points = []
  for distance in distances:
    min_distance = find_json_by('code', min_distances, distance['code'])
    point = min_distance['value'] / distance['value']
    points.append({ "building_id": distance['building_id'], "code": distance['code'], "value": point })

  for building in buildings_json_data:
    total_dx = 0
    for dx_param in dx_params:
      point = find_json_by_two_conditions(['code', 'building_id'], points, [dx_param['code'], building['id']])
      value = round(point['value'] * dx_param['weight'], 4)

      # Saving performance
      assessments.append({ "building_id": building['id'], "code": dx_param['code'], "point": point['value'], "weight": dx_param['weight'], "value": value })

      total_dx += value

    # Saving bx into building
    building['dx'] = round(total_dx, 4)

  filename = os.path.join(my_dir, 'data/assessments.json')
  os.makedirs(os.path.dirname(filename), exist_ok=True)

  with open(filename, 'w') as file:
    json.dump(assessments, file, indent=2, separators=(',', ': '))
    file.write('\n')  # Adding new line

  for building in buildings_json_data:
    value = building['ax'] + building['bx'] + building['cx'] + building['dx']
    building['performance'] = round(value, 4)

    # Adding level
    if value >= 0.45 and value <= 0.65:
      building['level'] = 'Bronze'
    elif value > 0.65 and value <= 0.85:
      building['level'] = 'Silver'
    elif value > 0.85 and value <= 1.0:
      building['level'] = 'Gold'
    else:
      building['level'] = 'Not eligible'

  filename = os.path.join(my_dir, 'data/buildings.json')
  os.makedirs(os.path.dirname(filename), exist_ok=True)

  with open(filename, 'w') as file:
    json.dump(buildings_json_data, file, indent=2, separators=(',', ': '))
    file.write('\n')  # Adding new line

  return redirect(url_for('show', id= id))

def find_json_by(key, array, id):
  for item in array:
    if item[key] == id:
      return item
  return None

def find_json_by_two_conditions(keys, array, values):
  for item in array:
    if item[keys[0]] == values[0] and item[keys[1]] == values[1]:
      return item
  return None

def calculate_slope(time_series):
  n = len(time_series)

  # Calculate the mean of x (time indices) and y (time series values)
  mean_x = sum(range(n)) / n
  mean_y = sum(time_series) / n

  # Calculate the slope (m) of the regression line
  numerator = sum((i - mean_x) * (y - mean_y) for i, y in enumerate(time_series))
  denominator = sum((i - mean_x) ** 2 for i in range(n))

  slope = numerator / denominator

  return slope

if __name__ == '__main__':
  app.run()