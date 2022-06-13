from flask import Flask, render_template, request
from datetime import datetime
import json, re
import urllib.request

app = Flask(__name__)

@app.route('/', methods =['POST', 'GET'])
def weather():
	try:
		if request.method == 'POST':
			city = request.form['city']
		else:
			city = 'jaipur'

		api = 'dcb7e9e91cf57bcda6c81f988634ab0d'

		city = city.title()
		city = re.sub(' +', ' ', city.strip())
		city_new = city.replace(" ", "+")

		source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city_new + '&appid=' + api).read()
		list_of_data = json.loads(source)

		temp_cel = list_of_data['main']['temp']
		temp_cel = temp_cel - 273.15
		temp_cel = round(temp_cel, 2)
		temp_cel = f'{temp_cel}\u00B0c'

		temp_max = list_of_data['main']['temp_max']
		temp_max = temp_max - 273.15
		temp_max = round(temp_max, 2)
		temp_max = f'{temp_max}\u00B0c'

		temp_min = list_of_data['main']['temp_min']
		temp_min = temp_min - 273.15
		temp_min = round(temp_min, 2)
		temp_min = f'{temp_min}\u00B0c'

		wind_deg = list_of_data['wind']['deg']
		wind_deg = f'{wind_deg}\u00B0c'

		sunrise = list_of_data['sys']['sunrise']
		sunrise = datetime.fromtimestamp(sunrise)
		sunrise = sunrise.strftime("%H:%M")

		sunset = list_of_data['sys']['sunset']
		sunset = datetime.fromtimestamp(sunset)
		sunset = sunset.strftime("%H:%M")

		lon = list_of_data['coord']['lon']
		lon = round(lon, 2)

		lat = list_of_data['coord']['lat']
		lat = round(lat, 2)

		visibility = list_of_data['visibility']
		visibility = visibility/100

		data = {
			"cityname": city,
			"country_code": str(list_of_data['sys']['country']),
			"sunrise": sunrise,
			"sunset": sunset,
			"lon": lon,
			"lat": lat,
			"temp": str(list_of_data['main']['temp']) + 'k',
			"temp_cel": temp_cel,
			"temp_min": temp_min,
			"temp_max": temp_max,
			"humidity": str(list_of_data['main']['humidity']) + '%',
			"icon": str(list_of_data['weather'][0]['icon']),
			"main": str(list_of_data['weather'][0]['description']),
			"visibility": str(visibility) + '%',
			"wind_speed": str(list_of_data['wind']['speed']) + " k/h",
			"wind_deg": wind_deg
		}
		return render_template('index.html', data=data)
	except:
		data={
			"error": "doesn't Exists.",
			"cityname": city
		}
		return render_template('index.html', data=data)

if __name__ == '__main__':
	app.run(debug = True)
