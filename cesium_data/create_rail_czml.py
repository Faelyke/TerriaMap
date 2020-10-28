import json
from czml import czml # python3.8:  pip install czml 
import random
import datetime
import math


# workaround, as CZML is broken.
class DummyObject(str):
    def __init__(self, data):
        self._data = data
    def data(self):
        return self._data
    
payload = None
points_db = []

def get_closest_point(point, rail_index):
    distance = 9999
    mdi = 0
    for index, cached_points in enumerate(points_db):
        if (index != rail_index):
            cached_first_point = (cached_points[0], cached_points[1]) # no Z
            cached_last_point = (cached_points[-1], cached_points[-2]) # no Z
            distance_ = math.sqrt(
                (point[0] - cached_first_point[0])**2  + (point[1] - cached_first_point[1])**2
            )
            if distance_ < distance:
                distance = distance_
                mdi = index
            distance_ = math.sqrt(
                (point[0] - cached_last_point[0])**2  + (point[1] - cached_last_point[1])**2
            )
            if distance_ < distance:
                distance = distance_
                mdi = index
    print(distance)
    return points_db[mdi], distance

def multilinestring_to_positions(rail, join_nearest_rail=False, index=0):
    path = rail['path']
    path = path.replace("MULTILINESTRING ", "")
    path = path.replace("((", "")
    path = path.replace("))", "")

    path = path.split(",")
    #print(path)
    points = []
    for point in path:
        p = point
        p_original = point
        if p[0] == " ":
            p = p[1:]
            #print(p)
        p = point.replace(" ", ',')
        
        p = p.split(",")
        if len(p) > 0:
            if (p[0] == ''):
                p_f = (float(p[1]), float(p[2]), 0)
            else:
                p_f = (float(p[0]), float(p[1]), 0)
        else:
            print("zero",point)
        #print(p)
        #p_f = (float(p[0]), float(p[1]))
        
        points.append(p_f[0])
        points.append(p_f[1])
        points.append(p_f[2])
    #print(points)

    if join_nearest_rail and index < len(payload)-1:
        other_point, distance = get_closest_point((points[-1], points[-2]), index)
        if distance < 0.008:
            points.append(other_point[0])
            points.append(other_point[1])
            points.append(0)

    return points


with open("custom_rails_202010281149.json", 'r') as f:
    payload = json.loads(f.read())['custom_rails']


doc = czml.CZML()

initial_packet =  czml.CZMLPacket(id="document", version="1.0")
initial_packet.clock = {
            "step": "SYSTEM_CLOCK_MULTIPLIER",
            "range": "LOOP_STOP",
            "multiplier": 2160000/600,
            "interval": "2020-01-01/2030-01-01",
            "currentTime": "2020-01-01"
        }
initial_packet.name = "IORAMA Rails"
doc.packets.append(initial_packet)

# fill cached points
for rail in payload:
    points_db.append(multilinestring_to_positions(rail, False, -1))

for index, rail in enumerate(payload):
    positions = multilinestring_to_positions(rail, False, index)




    packet = czml.CZMLPacket(id=rail['segment'].lower().replace(' ', "") , status="t")#id=str(random.randint(0, 99999)), name=rail['segment'])
    packet._name = rail['segment']
    packet._description = DummyObject(rail['segment'])
    
    props = list(packet._properties)
    props.append("status")
    packet._properties = props
    #print(packet._properties)
    packet.status = DummyObject(rail['new_track'])
    #packet._description = "t"#str(rail['new_track'])

    positions = czml.Positions(cartographicDegrees=positions)

    pl = czml.Polyline(positions=positions)
    if rail['new_track'].lower() == "new":
        color = {'rgba': [255, 0,0,255]}
    else:
        color = {'rgba': [0, 0,255,255]}
    pl.material = czml.Material(solidColor=czml.SolidColor(color=color))
    pl.width = 5
    pl.clampToGround = True
    
    packet.polyline = pl
    doc.packets.append(packet)

filename = "../wwwroot/test/rails.czml"
doc.write(filename)