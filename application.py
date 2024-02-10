from flask import Flask, request, render_template, redirect, url_for, Response, send_file
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

@app.route('/api/assessments')
def api_assessments():
  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      buildings = json.load(file)
  except FileNotFoundError:
    buildings = []

  try:
    filename = os.path.join(my_dir, 'data/assessments.json')

    with open(filename, 'r') as file:
      assessments = json.load(file)
  except FileNotFoundError:
    assessments = []

  try:
    filename = os.path.join(my_dir, 'parameters.json')

    with open(filename, 'r') as file:
      parameters = json.load(file)
  except FileNotFoundError:
    parameters = []

  for assessment in assessments:
    building = find_json_by('id', buildings, assessment['building_id'])
    parameter = find_json_by('code', parameters, assessment['code'])
    assessment['building_level'] = building['level']
    assessment['building_city'] = building['city']
    assessment['parameter_group'] = parameter['group']
    assessment['parameter_category'] = parameter['category']

  json_data = json.dumps(assessments, indent=2, separators=(',', ': '))
  return Response(response=json_data, status=200, content_type='application/json')

@app.route('/api/consumptions')
def api_consumptions():
  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      buildings = json.load(file)
  except FileNotFoundError:
    buildings = []

  try:
    filename = os.path.join(my_dir, 'parameters.json')

    with open(filename, 'r') as file:
      parameters = json.load(file)
  except FileNotFoundError:
    parameters = []

  cx_params = []
  for sub in parameters:
    if sub['group'] == 'cx':
      cx_params.append(sub)

  consumptions = []
  for building in buildings:
    for cx_param in cx_params:
      parameter = find_json_by('code', parameters, cx_param['code'])
      months = [1, 2, 3, 4, 5, 6]

      for month in months:
        consumptions.append({'building_id': building['id'], 'name': building['name'], 'month': month, 'code': cx_param['code'], 'value': building[f"{cx_param['code']}_{month}"]})

  json_data = json.dumps(consumptions, indent=2, separators=(',', ': '))
  return Response(response=json_data, status=200, content_type='application/json')

@app.route('/api/buildings')
def api_buildings():
  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      buildings = json.load(file)
  except FileNotFoundError:
    buildings = []

  try:
    filename = os.path.join(my_dir, 'parameters.json')

    with open(filename, 'r') as file:
      parameters = json.load(file)
  except FileNotFoundError:
    parameters = []

  try:
    filename = os.path.join(my_dir, 'data/assessments.json')

    with open(filename, 'r') as file:
      assessments = json.load(file)
  except FileNotFoundError:
    assessments = []

  for building in buildings:
    total_policy = 0
    total_retrofit = 0
    total_construction = 0
    total_utilization = 0
    for assessment in assessments:
      if building['id'] == assessment['building_id']:
        parameter = find_json_by('code', parameters, assessment['code'])
        if parameter['category'] == 'Policy':
          total_policy += assessment['value']
        elif parameter['category'] == 'Retrofit':
          total_retrofit += assessment['value']
        elif parameter['category'] == 'Construction':
          total_construction += assessment['value']
        else:
          total_utilization += assessment['value']
    building['policy'] = round(total_policy, 4)
    building['retrofit'] = round(total_retrofit, 4)
    building['construction'] = round(total_construction, 4)
    building['utilization'] = round(total_utilization, 4)

  json_data = json.dumps(buildings, indent=2, separators=(',', ': '))
  return Response(response=json_data, status=200, content_type='application/json')

@app.route('/api/buildings', methods=['POST'])
def create_buildings():
  form_data = request.get_json()
  create_building(form_data)
  evaluate_buildings()

  json_data = json.dumps(form_data, indent=2, separators=(',', ': '))
  return Response(response=json_data, status=200, content_type='application/json')

@app.route('/api/buildings/<int:id>')
def show_building(id):
  building = show_building(id)
  json_data = json.dumps(building, indent=2, separators=(',', ': '))
  return Response(response=json_data, status=200, content_type='application/json')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/buildings')
def buildings():
  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      buildings = json.load(file)
  except FileNotFoundError:
    buildings = []

  return render_template('buildings.html', buildings=buildings)

@app.route('/buildings/new')
def new():
  # Adding default value in the new form
  data = '{"name": "", "p01": "Yes", "p02": "Yes", "p03": "Yes", "p04": "Yes", "p05": "Yes", "p06": "Yes", "p07": "Yes", "p08": "Yes", "p09": "Yes", "p10": "Yes", "p11": "Yes", "p12": "Yes", "p13": "Yes", "p14": "Yes", "p15": "Yes", "p16": "Yes", "p17": "Yes", "p18": "Yes", "p19": "Yes", "p20": "Yes", "p21": "Yes", "p22": "Yes", "p23": "Yes", "p24": "Yes", "p25": "Yes", "p26": "Yes", "p27": "Yes", "p28": "Yes", "p29": "Yes", "p30": "Yes", "p31": "Yes", "p32": "Yes", "p33": 0.0, "p34": 675, "p35": "Yes", "p36": "Yes", "p37": "Yes", "p38": "Yes", "p39": "Yes", "p40": "Yes", "p41": "Yes", "p42": "Yes", "p43": "Yes", "p44": "Yes", "p45": "Yes", "p46": "Yes", "p47": "Yes", "p48": "Yes", "p49": "Yes", "p50": "Yes", "p51_1": 3000, "p51_2": 4000, "p51_3": 5000, "p51_4": 4000, "p51_5": 7000, "p51_6": 1500, "p52": "Yes", "p53": "Yes", "p54": "Yes", "p55": "Yes", "p56": "Yes", "p57": "Yes", "p58": "Yes", "p59": "Yes", "p60": "Yes", "p61_1": 4000000.0, "p61_2": 5000000.0, "p61_3": 4000000.0, "p61_4": 4000000.0, "p61_5": 5000000.0, "p61_6": 4400000.0, "p62": "Yes", "p63": 500000000.0, "p64": "Yes", "p65": "Yes", "p66": "Yes", "p67_1": 5.0, "p67_2": 5.0, "p68_1": 4000000.0,  "p68_2": 4000000.0, "p68_3": 4000000.0, "p68_4": 4000000.0, "p68_5": 4000000.0, "p68_6": 4200000.0, "p69": 10000000.0, "p70": "Yes", "p71": "2022-12-09", "p72": 23.0, "p73": 36, "p74": "Yes", "p75": "Yes", "p76": "Yes", "p77": "Yes", "p78": "Yes", "p79_1": 33.48, "p79_2": 32.40, "p79_3": 34.56, "p79_4": 29.64, "p79_5": 16.44, "p79_6": 35.76,  "p80": "Yes", "p81": "Yes", "p82": "Yes", "p83": "Yes"}'
  building = json.loads(data)
  return render_template('new.html', building=building)

@app.route('/buildings', methods=['POST'])
def create():
  form_data = request.form.to_dict()
  create_building(form_data)
  return redirect(url_for('show', id= form_data['id']))

@app.route('/buildings/<int:id>')
def show(id):
  # Reading JSON file
  building = show_building(id)
  return render_template('show.html', building=building)

@app.route('/buildings/<int:id>/evaluate', methods=['POST'])
def evaluate(id):
  evaluate_buildings()
  return redirect(url_for('show', id= id))

@app.route('/download_android_apk')
def download_android_apk():
  return send_file('app-green-building.apk', as_attachment=True)

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

def create_building(form_data):
    # Reading JSON file
  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      json_data = json.load(file)
  except FileNotFoundError:
    json_data = []

  # Changing string data type into correct one
  form_data['id'] = json_data[0].get('id', 0) + 1 if len(json_data) else 1
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

  # Adding form_data to json_data array
  json_data.insert(0, form_data)

  # Saving array json_data into JSON file
  filename = os.path.join(my_dir, 'data/buildings.json')
  os.makedirs(os.path.dirname(filename), exist_ok=True)

  with open(filename, 'w') as file:
    json.dump(json_data, file, indent=2, separators=(',', ': '))
    file.write('\n')  # Adding new line

def evaluate_buildings():
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
        try:
          point = calculate_p33(building[bx_param['code']])
        except Exception as e:
          point = 0

      if bx_param['code'] == 'p34':
        try:
          point = calculate_p34(building[bx_param['code']])
        except Exception as e:
          point = 0

      if bx_param['code'] == 'p63':
        # pre-processing
        raw_p63 = (building['p61_6'] - building['p63']) / building['p63']
        try:
          point = calculate_p63(raw_p63)
        except Exception as e:
          point = 0

      if bx_param['code'] == 'p69':
        # pre-processing
        raw_p69 = (building['p68_6'] - building['p69']) / building['p69']
        try:
          point = calculate_p69(raw_p69)
        except Exception as e:
          point = 0

      if bx_param['code'] == 'p71':
        # pre-processing
        start = datetime.strptime(building['p71'], "%Y-%m-%d")
        end = datetime.now()
        res = (end.year - start.year) * 12 + (end.month - start.month)
        raw_p71 = res
        try:
          point = calculate_p71(raw_p71)
        except Exception as e:
          point = 0

      if bx_param['code'] == 'p72':
        try:
          point = calculate_p72(building[bx_param['code']])
        except Exception as e:
          point = 0

      if bx_param['code'] == 'p73':
        try:
          point = calculate_p73(building[bx_param['code']])
        except Exception as e:
          point = 0

      value = round(point * bx_param['weight'], 4)

      # Saving performance
      assessments.append({ "building_id": building['id'], "code": bx_param['code'], "point": round(point, 4), "weight": bx_param['weight'], "value": value })

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
      assessments.append({ "building_id": building['id'], "code": cx_param['code'], "point": round(point['value'], 4), "weight": cx_param['weight'], "value": value })

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
      assessments.append({ "building_id": building['id'], "code": dx_param['code'], "point": round(point['value'], 4), "weight": dx_param['weight'], "value": value })

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

def show_building(id):
  try:
    filename = os.path.join(my_dir, 'data/buildings.json')

    with open(filename, 'r') as file:
      buildings = json.load(file)
  except FileNotFoundError:
    buildings = []

  return find_json_by('id', buildings, id)

if __name__ == '__main__':
  app.run()