from asyncio import LimitOverrunError
from curses import meta
from datetime import date, datetime,timedelta
from math import sin,cos,tan,floor
from re import L
import re
from tkinter import E, Label
#from pickletools import read_uint1
from Selfmade.Ransom import Usefull_stuff
import psutil
import GPUtil
import meteostat
import logging
import pandas as pd

#logging = logging.getLogger(__name__)
config={}

class ext_func:
    cachedTime=None
    LastCall=-1
    LastUpdatedWeatherInfo=None
    cachedWeatherInfo=None
    def perx(percent:list[float]):
        return (percent[1],round((percent[2] - percent[1])*(percent[0]/100) + percent[1],0))
    def get_Time(Frame:int) -> datetime:
        if ext_func.LastCall != Frame:
            ext_func.LastCall=Frame
            ext_func.cachedTime=datetime.now()
        return ext_func.cachedTime
    def updateWeatherInfo():
        if  (not (ext_func.LastUpdatedWeatherInfo == None or ext_func.cachedWeatherInfo == None)) and (ext_func.LastUpdatedWeatherInfo - datetime.now() < timedelta(hours=1)):
            return ext_func.cachedWeatherInfo
        logging.info(f"Re-Generating Weather-Info...")
        location = meteostat.Point(config["Location"][0],config["Location"][1])

        yearago=datetime.now().replace(year=datetime.now().year-1,hour=0,minute=0,second=0)

        # station, time, temp, dwpt (dew point), rhum (humidity), prcp (precipitation), snow, wdir (wind direction), wspd (wind speed), wpgt (peak wind gust), pres (pressure), tsun (sunshine), coco (weather condition)
        DirtyDataToday:pd.DataFrame = meteostat.Hourly(location, datetime.now().replace(hour=0,minute=0,second=0), datetime.now().replace(hour=23,minute=59,second=59)) # Get hourly data for today
        # station, time, tavg (average temperature), tmin (minimum temperature), tmax (maximum temperature), dwpt (dew point), rhum (humidity), prcp (precipitation),
        # snow, wdir (wind direction), wspd (wind speed), wpgt (peak wind gust), pres (pressure), tsun (sunshine), coco (weather condition)
        DirtyDataYear:pd.DataFrame = meteostat.Daily(location, yearago-timedelta(weeks=8), yearago+timedelta(weeks=8)) # Get daily data for the last year
        DirtyDataToday:pd.DataFrame = DirtyDataToday.fetch()
        DirtyDataYear:pd.DataFrame = DirtyDataYear.fetch()

        #////////////////////////////////////////////// DATA NORMALIZATION //////////////////////////////////////////////////

        #Agregrate data for past Year: [tmean, tmin, tmax, [prcpWinter,prcpSpring,prcpSummer,prcpFall], [snowWinter,snowSpring,snowSummer,snowFall],wspd,tsunmean,tsunmin,tsunmax]

        DirtyDataYear = DirtyDataYear[DirtyDataYear["prcp"] >0.5]
        LightRainLimit = DirtyDataYear["prcp"].quantile(0.7)
        HeavyRainLimit = DirtyDataYear["prcp"].quantile(0.9)

        DirtyDataYear["snow"] = DirtyDataYear["snow"].map(lambda x: x/10)
        DirtyDataYear = DirtyDataYear[DirtyDataYear["snow"] >0.5]
        LightSnowLimit = DirtyDataYear["snow"].quantile(0.7)
        HeavySnowLimit = DirtyDataYear["snow"].quantile(0.9)

        DirtyDataYear = DirtyDataYear[DirtyDataYear["wspd"] >5.5]
        LightWindLimit = DirtyDataYear["wspd"].quantile(0.7)
        HeavyWindLimit = DirtyDataYear["wspd"].quantile(0.9)



        dataYear = {"temp":{"value":DirtyDataToday["temp"].mean(),"tavg":DirtyDataYear["tavg"].mean(),"tmin":DirtyDataYear["tmin"].mean(),"tmax":DirtyDataYear["tmax"].mean()},
                    "prcp":{"value":float(DirtyDataToday["prcp"].sum()),"LightRainLimit":LightRainLimit,"HeavyRainLimit":HeavyRainLimit},
                    "snow":{"value":float(DirtyDataToday["snow"].sum()),"direction":DirtyDataToday["wdir"].mean(),"LightSnowLimit":LightSnowLimit,"HeavySnowLimit":HeavySnowLimit}}
        
        for x in dataYear.keys():
            for y in dataYear[x].keys():
                dataYear[x][y] = round(dataYear[x][y],2)


        ext_func.LastUpdatedWeatherInfo = datetime.now()
        ext_func.cachedWeatherInfo = dataYear
        logging.info(f"DONE: Weather-Info updated")
        return dataYear

def __entry__(ent_config:str) -> None:
    global config
    logging.info("Loading Module: functions.py")
    config = ent_config
    ext_func.cachedTime = datetime.now()



class call_func:
    ltp=0
    ekh=Usefull_stuff.Timer(True)
    fps=0
    lst=0
    refefe=20
    cgr=refefe
    lastest=[(0,0),(0,0),(0,0)]
    _LASTCALL=0
    weatherShownItems=3
    ExtreemeWeather=False
    errorvals={
        "dt":"0:0:0 | 0.0.0",
        "dayshort":"N/A",
        "cpu_usage":(0,0),
        "gpu_usage":(0,0),
        "ram_usage":(0,0),
        "frame":"0",
        "rainbow":(0,0,0),
        "mv":(0,0),
        "Portal":"Portal/1",
        "weatherInf":"N/A",
        "weatherSize":26,
        "weatherPic":"WeatherIcons/2682803_weather_exclamation_attention_mark_erro_warn_warning"
    }
    def __error__(func_name:str) -> any:
        """Function for returning a default value if error in script occurs"""
        return call_func.errorvals.get(func_name,f"key for {func_name} not found")
    def dt(id,call) -> str:
        now = ext_func.get_Time(call)
        return now.strftime("%H:%M:%S | %d.%m.%y")
    def dayshort(id,call) -> str:
        now = ext_func.get_Time(call)
        return now.strftime("%A")[:3]
    def weatherInf(id,call) -> str:
        weather = ext_func.updateWeatherInfo()
        Items = 3
        out = f"Temp: {weather["temp"]["value"]}°C\nmax: {weather["temp"]["tmax"]}°C\nmin: {weather["temp"]["tmin"]}°C"
        if weather["prcp"]["value"] > weather["prcp"]["LightRainLimit"]:
            out += f"\nRain: {weather["prcp"]["value"]}mm"
            Items+=1
        if weather["snow"]["value"] > weather["snow"]["LightSnowLimit"]:
            out += f"\nSnow: {weather["snow"]["value"]}mm"
            Items+=1
        call_func.weatherShownItems = Items
        return out
    def weatherSize(id,call) -> int:
        if call_func.weatherShownItems == 3:
            return 36
        elif call_func.weatherShownItems == 4:
            return 31
        else:
            return 26
    def weatherPic(id,call) -> str:
        weather = ext_func.updateWeatherInfo()
        if id == 3:
            if ext_func.get_Time(call).hour >= 20 or ext_func.get_Time(call).hour <= 6:
                out = "WeatherIcons/2682801_mist_moon_cloudy_fog_weather_night_foggy"
            else:
                out = "WeatherIcons/2682848_sunny_weather_forecast_day_sun"
            Raintype = 0
            if weather["prcp"]["value"] >= weather["prcp"]["LightRainLimit"]:
                Raintype = 1
                out = "WeatherIcons/2682837_weather_forecast_rain_drop_sun_day_cloud"
            elif weather["prcp"]["value"] >= weather["prcp"]["HeavyRainLimit"]:
                Raintype = 2
                out = "WeatherIcons/2682835_precipitation_weather_forecast_cloudy_rainy_cloud_rain"
            elif weather["prcp"]["value"] >= weather["prcp"]["HeavyRainLimit"]*2:
                Raintype = 3
                out = "WeatherIcons/2682807_rain_high_weather_percentage_precipitation_drop_humidity"
            Snowtype = 0
            if weather["snow"]["value"] >= weather["snow"]["LightSnowLimit"] and Raintype == 0:
                Snowtype = 1
                out = "WeatherIcons/2682815_precipitation_sun_snow_forecast_weather_day_cloud"
            elif weather["snow"]["value"] >= weather["snow"]["HeavySnowLimit"] and Raintype <= 2:
                Snowtype = 2
                out = "WeatherIcons/2682823_snow_weather_snowflake_forecast"
            elif weather["snow"]["value"] >= weather["snow"]["HeavySnowLimit"]*2:
                Snowtype = 3
                out = "WeatherIcons/2682823_snow_weather_snowflake_forecast"
            if Raintype == 3 and Snowtype == 3:
                call_func.ExtreemeWeather = True
            return out
        elif id == 4:
            if call_func.ExtreemeWeather:
                return "WeatherIcons/2682803_weather_exclamation_attention_mark_erro_warn_warning"
            if weather["temp"]["value"] <= 27:
                return "WeatherIcons/2682809_winter_cold_termometer_low_weather_freezing_temperature"
            elif weather["temp"]["value"] <= 32:
                return "WeatherIcons/2682808_temperature_high_hot_weather_termometer_summer"
            return "WeatherIcons/2682803_weather_exclamation_attention_mark_erro_warn_warning"
        else:
            return "WeatherIcons/2682803_weather_exclamation_attention_mark_erro_warn_warning"
        
    def cpu_usage(id,call) -> int:
        if call_func.cgr >= call_func.fps:
            call_func.lastest[0] = ext_func.perx((psutil.cpu_percent(),180+66,270+24))
        return call_func.lastest[0]
    def gpu_usage(id,call) -> int:
        if call_func.cgr >= call_func.fps:
            call_func.lastest[1] = ext_func.perx((GPUtil.getGPUs()[0].load*100,180+66,270+24))
        return call_func.lastest[1]
    def ram_usage(id,call) -> int:
        if call_func.cgr >= call_func.fps:
            call_func.lastest[2] = ext_func.perx((psutil.virtual_memory().percent,180+66,270+24))
            call_func.cgr=0
        call_func.cgr+=1
        return call_func.lastest[2]
    def frame(id,call) -> str:
        if call_func.ekh.timer(1):
            call_func.fps= call - call_func.lst
            call_func.lst=call
            call_func.ekh.reset()
        return str(call_func.fps)
    def rainbow(id,call):
        return (abs(round(255*sin(call*3))),abs(round(255*cos(call*0.5))),abs(round(255*tan(call*0.1))))
    def mv(id,call):
        #[1000,200]
        return (1000+100*sin(call*0.1),200+100*cos(call*0.1))
    def Portal(id,call):
        call_func.ltp+=1
        if call_func.ltp >= 19:call_func.ltp=1
        return str(f"Portal/{call_func.ltp}")