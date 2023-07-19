from flask import Flask, request, render_template, redirect, url_for
import numpy as np
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

app = Flask(__name__)

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

@app.route('/')
def index():
  try:
    with open('data/buildings.json', 'r') as file:
      buildings = json.load(file)
  except FileNotFoundError:
    buildings = []

  try:
    with open('data/performances.json', 'r') as file:
      performances = json.load(file)
  except FileNotFoundError:
    performances = []

  for building in buildings:
    performance = find_json_by('building_id', performances, building['id'])
    if performance:
      building['performance'] = round((performance['ax'] + performance['bx'] + performance['cx'] + performance['dx']) * 100, 2)
    else:
      building['performance'] = '-'

  return render_template('index.html', buildings=buildings)

@app.route('/buildings/new')
def new():
  # Adding default value in the new form
  data = '{"name": "G05", "p01": "No", "p02": "Yes", "p03": "Yes", "p04": "Yes", "p05": "Yes", "p06": "Yes", "p07": "No", "p08": "No", "p09": "Yes", "p10": "Yes", "p11": "Yes", "p12": "Yes", "p13": "Yes", "p14": "Yes", "p15": "Yes", "p16": "Yes", "p17": "Yes", "p18": "Yes", "p19": "Yes", "p20": "Yes", "p21": "Yes", "p22": "Yes", "p23": "Yes", "p24": "Yes", "p25": "Yes", "p26": "Yes", "p27": "No", "p28": "Yes", "p29": "No", "p30": "Yes", "p31": "Yes", "p32": "No", "p33": 0, "p34": 675, "p35": "Yes", "p36": "Yes", "p37": "No", "p38": "No", "p39": "No", "p40": "Yes", "p41": "No", "p42": "No", "p43": "No", "p44": "Yes", "p45": "No", "p46": "No", "p47": "No", "p48": "No", "p49": "Yes", "p50": "Yes", "p51_1": 3000, "p51_2": 4000, "p51_3": 5000, "p51_4": 4000, "p51_5": 7000, "p51_6": 1500, "p52": "No", "p53": "Yes", "p54": "Yes", "p55": "Yes", "p56": "Yes", "p57": "Yes", "p58": "Yes", "p59": "Yes", "p60": "Yes", "p61_1": 4000000.0, "p61_2": 5000000.0, "p61_3": 4000000.0, "p61_4": 4000000.0, "p61_5": 5000000.0, "p61_6": 4400000.0, "p62": "Yes", "p63": 500000000, "p64": "Yes", "p65": "Yes", "p66": "Yes", "p67_1": 5.0, "p67_2": 5.0, "p68_1": 4000000,  "p68_2": 4000000, "p68_3": 4000000, "p68_4": 4000000, "p68_5": 4000000, "p68_6": 4200000, "p69": 10000000, "p70": "Yes", "p71": "2022/12/09", "p72": 23.0, "p73": 36, "p74": "No", "p75": "Yes", "p76": "Yes", "p77": "Yes", "p78": "Yes", "p79_1": 33.48, "p79_2": 32.40, "p79_3": 34.56, "p79_4": 29.64, "p79_5": 16.44, "p79_6": 35.76,  "p80": "Yes", "p81": "Yes", "p82": "No", "p83": "Yes"}'
  building = json.loads(data)
  return render_template('new.html', building=building)

@app.route('/buildings', methods=['POST'])
def create():
  form_data = request.form.to_dict()

  # Reading JSON file
  try:
    with open('data/buildings.json', 'r') as file:
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
  with open('data/buildings.json', 'w') as file:
    json.dump(json_data, file, indent=2, separators=(',', ': '))
    file.write('\n')  # Adding new line

  return redirect(url_for('show', id= form_data['id']))

@app.route('/buildings/<int:id>')
def show(id):
  # Reading JSON file
  try:
    with open('data/buildings.json', 'r') as file:
      buildings = json.load(file)
  except FileNotFoundError:
    buildings = []

  try:
    with open('data/performances.json', 'r') as file:
      performances = json.load(file)
  except FileNotFoundError:
    performances = []

  building = find_json_by('id', buildings, id)

  performance = find_json_by('building_id', performances, id)
  if performance:
    building['performance'] = round((performance['ax'] + performance['bx'] + performance['cx'] + performance['dx']) * 100, 2)

  return render_template('show.html', building=building)

@app.route('/buildings/<int:id>/evaluate', methods=['POST'])
def evaluate(id):
  # Reading JSON file
  try:
    with open('./parameters.json', 'r') as file:
      parameters_json_data = json.load(file)
  except FileNotFoundError:
    parameters_json_data = []

  try:
    with open('data/buildings.json', 'r') as file:
      buildings_json_data = json.load(file)
  except FileNotFoundError:
    buildings_json_data = []

  # ax
  ax_params = []
  for sub in parameters_json_data:
    if sub['group'] == 'ax':
      ax_params.append(sub)

  performances = []
  for building in buildings_json_data:
    value = 0
    for ax_param in ax_params:
      # encoding
      if building[ax_param['code']] == 'Yes':
        point = 1
      else:
        point = 0

      value += point * ax_param['weight']

    # Saving ax into performances
    performances.append({ "id": building['id'], "building_id": building['id'], "ax": value })

  # bx
  bx_params = []
  for sub in parameters_json_data:
    if sub['group'] == 'bx':
      bx_params.append(sub)

  for building in buildings_json_data:
    value = 0
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

      value += point * bx_param['weight']

    # Saving bx into performances
    for item in performances:
      if item['building_id'] == building['id']:
        item['bx'] = value

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

      slope = np.polyfit(months, values, 1)[0]
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
    value = 0
    for cx_param in cx_params:
      point = find_json_by_two_conditions(['code', 'building_id'], points, [cx_param['code'], building['id']])
      value += point['value'] * cx_param['weight']

    # Saving bx into performances
    for item in performances:
      if item['building_id'] == building['id']:
        item['cx'] = value

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
    value = 0
    for dx_param in dx_params:
      point = find_json_by_two_conditions(['code', 'building_id'], points, [dx_param['code'], building['id']])
      value += point['value'] * dx_param['weight']

    # Saving bx into performances
    for item in performances:
      if item['building_id'] == building['id']:
        item['dx'] = value

  with open('data/performances.json', 'w') as file:
    json.dump(performances, file, indent=2, separators=(',', ': '))
    file.write('\n') # Adding new line
  
  return redirect(url_for('show', id= id))
