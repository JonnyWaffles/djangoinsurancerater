import os, sys, csv
from models import Exposure

def setUp():
    with open(os.path.join(sys.path[0], 'djangoinsurancerater/ExposureByEmployeeCountandLimit.csv')) as f:
      reader = csv.reader(f)
      for row in reader:
        _, created = Exposure.objects.get_or_create(
        number_employees = row[0],
        insurance_limit = row[1],
        exposure_points = row[2],
        )
setUp()