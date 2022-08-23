
import paho.mqtt.client as mqtt 
from random import randrange, uniform
import growattServer


#Put in username from server.growatt.com
username="USERNAME"

#Put in password from server.growatt.com
user_pass="PASSWORD"

api = growattServer.GrowattApi()
login_response = api.login(username, user_pass)

plant_list = api.plant_list(login_response['user']['id'])

for plant in plant_list['data']:
  plant_id = plant['plantId']
  plant_name = plant['plantName']
  plant_info=api.plant_info(plant_id)

  for device in plant_info['deviceList']:
    device_sn = device['deviceSn']
    device_type = device['deviceType']
    mix_info = api.mix_info(device_sn, plant_id)
    mix_totals = api.mix_totals(device_sn, plant_id)
    mix_detail = api.mix_detail(device_sn, plant_id)
    pacToGridToday = 0.0
    pacToUserToday = 0.0
    pdischargeToday = 0.0
    ppvToday = 0.0
    sysOutToday = 0.0

    chartData = mix_detail['chartData']
    for time_entry, data_points in chartData.items():
      pacToGridToday += float(data_points['pacToGrid']) * (5/60)
      pacToUserToday += float(data_points['pacToUser']) * (5/60)
      pdischargeToday += float(data_points['pdischarge']) * (5/60)
      ppvToday += float(data_points['ppv']) * (5/60)
      sysOutToday += float(data_points['sysOut']) * (5/60)

    mix_detail['calculatedPacToGridTodayKwh'] = round(pacToGridToday,2)
    mix_detail['calculatedPacToUserTodayKwh'] = round(pacToUserToday,2)
    mix_detail['calculatedPdischargeTodayKwh'] = round(pdischargeToday,2)
    mix_detail['calculatedPpvTodayKwh'] = round(ppvToday,2)
    mix_detail['calculatedSysOutTodayKwh'] = round(sysOutToday,2)


    dashboard_data = api.dashboard_data(plant_id)

    calculated_consumption = float(mix_detail['eChargeToday']) + float(mix_detail['echarge1']) + float(mix_detail['etouser'])

    solar_to_battery = round(float(mix_info['epvToday']) - float(mix_detail['eAcCharge']) - float(mix_detail['eChargeToday']),2)
    ac_to_battery = round(float(mix_info['eBatChargeToday']) - solar_to_battery,2)


    mix_status = api.mix_system_status(device_sn, plant_id)

    

#plant_id
plantId = plant['plantId']
#plant name
plantName = plant['plantName']
#deviceType
deviceType = device['deviceType']
#SerialNumber
deviceSn = device['deviceSn']
#Charging Batteries at (kw)
chargePower = mix_status['chargePower']
#Discharging Batteries at (kw)
pdisCharge1 = mix_status['pdisCharge1']
#Batteries
batteryPercent = mix_status['SOC']
#Solar Energy Today (kw)
todayEnergy =plant_info['todayEnergy']
#Solar Energy Total (kw)
totalEnergy = plant_info['totalEnergy']
#PV1 wattage
pPv1 = mix_status['pPv1']
#PV2 wattage
pPv2 = mix_status['pPv2']
#PV total wattage (API) - KW
pv_total = mix_status['ppv']
#Local load/consumption - KW
pLocalLoad = mix_status['pLocalLoad']
#Importing from Grid - KW
pactouser = mix_status['pactouser']
#Exporting to Grid - KW
pactogrid = mix_status['pactogrid']
#Battery Charge (kwh)
eBatChargeToday = mix_info['eBatChargeToday']
#Battery Discharge (kwh)
eBatDisChargeToday = mix_info['eBatDisChargeToday']
#Solar Generation (kwh)
epvToday = mix_info['epvToday']
#Local Load (kwh)
elocalLoadToday = mix_totals['elocalLoadToday']
#Export to Grid (kwh)
etoGridToday = mix_totals['etoGridToday']
#Battery Charge
eBatChargeTotal = mix_info['eBatChargeTotal']
#Battery Discharge (kwh)
eBatDisChargeTotal = mix_info['eBatDisChargeTotal']
#Solar Generation (kwh)
epvTotal = mix_info['epvTotal']
#Local Load (kwh)
elocalLoadTotal = mix_totals['elocalLoadTotal']
#Export to Grid (kwh)
etogridTotal = mix_totals['etogridTotal']
#Self generation total (batteries & solar - from API) (kwh)
eCharge = mix_detail['eCharge']
#Load consumed from solar (kwh)
eChargeToday = mix_detail['eChargeToday']
#Load consumed from batteries (kwh)
echarge1 = mix_detail['echarge1']
#Self consumption total (batteries & solar - from API) (kwh)
eChargeToday1 = mix_detail['eChargeToday1']
#Load consumed from grid (kwh)
etouser = mix_detail['etouser']
#Load consumption (API) (kwh)
elocalLoad = mix_detail['elocalLoad']
#Exported (kwh)
eAcCharge = mix_detail['eAcCharge']

#kwh to Watt conversion
pdisCharge1_w = float(mix_status['pdisCharge1'])*1000
pv_total_w = (float(mix_status['pPv1']) + float(mix_status['pPv2']))*1000

#PUT IN BROKER IP
mqttBroker ="123.123.123.123" 

client = mqtt.Client("growattApiToMqtt")
client.connect(mqttBroker) 


client.publish(f'growatt/{device_sn}/plantId', plantId)
client.publish(f'growatt/{device_sn}/plantName', plantName)
client.publish(f'growatt/{device_sn}/deviceType', deviceType)
client.publish(f'growatt/{device_sn}/deviceSn', deviceSn)
client.publish(f'growatt/{device_sn}/chargePower', chargePower)
client.publish(f'growatt/{device_sn}/totalEnergy', totalEnergy)
client.publish(f'growatt/{device_sn}/todayEnergy', todayEnergy)
client.publish(f'growatt/{device_sn}/pLocalLoad', pLocalLoad)
client.publish(f'growatt/{device_sn}/pactouser', pactouser)
client.publish(f'growatt/{device_sn}/pactogrid', pactogrid)
client.publish(f'growatt/{device_sn}/eBatChargeToday', eBatChargeToday)
client.publish(f'growatt/{device_sn}/eBatDisChargeToday', eBatDisChargeToday)
client.publish(f'growatt/{device_sn}/epvToday', epvToday)
client.publish(f'growatt/{device_sn}/elocalLoadToday', elocalLoadToday)
client.publish(f'growatt/{device_sn}/etoGridToday', etoGridToday)
client.publish(f'growatt/{device_sn}/eBatChargeTotal', eBatChargeTotal)
client.publish(f'growatt/{device_sn}/eBatDisChargeTotal', eBatDisChargeTotal)
client.publish(f'growatt/{device_sn}/epvTotal', epvTotal)
client.publish(f'growatt/{device_sn}/elocalLoadTotal', elocalLoadTotal)
client.publish(f'growatt/{device_sn}/etogridTotal', etogridTotal)
client.publish(f'growatt/{device_sn}/eCharge', eCharge)
client.publish(f'growatt/{device_sn}/eChargeToday', eChargeToday)
client.publish(f'growatt/{device_sn}/echarge1', echarge1)
client.publish(f'growatt/{device_sn}/eChargeToday1', eChargeToday1)
client.publish(f'growatt/{device_sn}/etouser', etouser)
client.publish(f'growatt/{device_sn}/elocalLoad', elocalLoad)
client.publish(f'growatt/{device_sn}/eAcCharge', eAcCharge)
client.publish(f'growatt/{device_sn}/soc', batteryPercent)
client.publish(f'growatt/{device_sn}/pPv1', pPv1)
client.publish(f'growatt/{device_sn}/pPv2', pPv2)
client.publish(f'growatt/{device_sn}/ppv', pv_total)
client.publish(f'growatt/{device_sn}/chargePower', chargePower)
client.publish(f'growatt/{device_sn}/pdisCharge1', pdisCharge1)
client.publish(f'growatt/{device_sn}/pv_total_w', pv_total_w)
client.publish(f'growatt/{device_sn}/pdisCharge1_w', pdisCharge1_w)
