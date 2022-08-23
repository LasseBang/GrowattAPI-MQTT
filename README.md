# GrowattAPI-MQTT
Utilize Growatt API to make API Data available over MQTT

I needed MQTT data to intergrate into Homey so decided to make this python script that take data from Growatt Server API and push all data out on MQTT.

You need 3 things to get this to work
1. Put in username and Password
2. Put in MQTT Broker IP
3. Create a cronjob to make this script run every 1minute

Type crontab -e on your Linux VM or Raspberry PI
Here is the command from my crontab
*/1 * * * * /usr/bin/python3 /home/python/mqtt.py
