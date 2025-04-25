**#Forecasting Daily Solar Panel Energy Production in İkitelli Using Weather Data**


In the modern energy sector, efficient operations and strategic decision-making are crucial. This project aims to develop a forecasting model that predicts daily solar panel energy production based on sunlight duration and associated weather conditions. The objective is to support energy trading decisions by providing accurate short-term predictions.

The developed forecasting model is expected to predict daily energy production with a high degree of accuracy. This prediction will be helpfull for applications in energy trading.

**Motivation:**

The primary goal is to optimize operational activities and enhance energy efficiency within the energy market. By accurately forecasting energy production, companies can better manage supply, reduce waste, and improve grid stability. 
Providing reliable forecasts allows stakeholders to make informed decisions in energy trading, ensuring that energy buying and selling are executed with maximum efficiency and minimum risk.

**Data Sources:**

The project uses publicly available data representing the daily energy production of a solar power plant located in Ikitelli, Istanbul for the year 2018. This dataset is provided by the 'Ulusal Akıllı Şehir Açık Veri Platformu'.
(https://data.ibb.gov.tr/dataset/893647c5-e85b-4d33-9f61-5aca98a27248/resource/52afa9a3-2ea1-420b-a783-505cfe635ece/download/ikitelli-gune-enerjisi-santrali-elektrik-uretim-miktarlar.xlsx)

To strengthen the model, historical weather data for Istanbul in 2018 will be integrated. This data includes key variables such as sunlight duration, temperature, and other meteorological conditions, and can be accessed from the WeatherSpark website.
https://tr.weatherspark.com/h/y/95434/2018/2018-y%C4%B1l%C4%B1-i%C3%A7in-%C4%B0stanbul-T%C3%BCrkiye-Tarihi-Hava-Durumu#Figures-Summary

https://www.meteoblue.com/tr/hava/haritas%C4%B1/index#coords=7.85/40.44/29.15&map=uvIndex~daily~auto~sfc~none
https://windy.app/tr/forecast2/spot/472239/T%C3%BCrkiye

**Data Analysis Methods:**

Solar panels are affected by many factors, including dust accumulation, pollution, hours of sunshine, shading, and temperature. While pollution and shading can be mitigated manually, sunshine duration and temperature are natural phenomena. In addition to the production data we obtained, I used cloud-cover and temperature datasets corresponding to the coordinates of the solar power plant located in the İkitelli/Halkalı  in Istanbul. The production figures were provided as an Excel file by the Ulusal Akıllı Şehir Açık Veri Platformu and cover the period from 1 May 2018 to 31 May 2019, presented in kWh. However, data for July 2018, October 2018, and January 2019 are missing.

To gather cloud-cover and temperature values, I first checked the WeatherSpark and MeteoBlue websites. However they require premium subscriptions and it was unclear whether I could download the data in the exact format I needed, I continued searching. Eventually, I found that the Open-Meteo website archives both cloud-cover and temperature data for Istanbul. After locating their API documentation, the remaining tasks were coding and exporting the results to Excel. Throughout the coding process I relied heavily on the pandas and matplotlib libraries.

**üretimdailymean.py** converts the raw Excel file from the plant operator—recorded at 15-minute intervals in daily production to daily total production in kWh.**(ikitelli_daily_energy.xlsx)**

**download_istanbul_weather.py** retrieves temperature and cloud-cover data for the plant’s latitude and longitude and saves them to Excel.**(daily_weather_2018-05_2019-05.xlsx)**

**birlestirilmisfinaldata.py** combines the two Excel tables into a cleaner dataset, producing train_data.xlsx. This dataset makes manipulation by machine-learning models much easier.**(train_data.xlsx)**

For data exploration I continued that a line-style histogram (i.e., line plots over time) would be the best, because daily sunshine, temperature, and energy-production values all vary continuously. The script **histogramtraindata.py** creates graph that includes plots of all three variables—temperature, cloud-cover, and daily energy production (kWh). Anyone viewing the chart can immediately understand how the variables relate to one another.

**NOTE: Codes and excell files will be converted to jupiter notebook in next step.**

**Hypothesis Testing**

**Cloud Cover and Production **: Whenever the orange production curve drops sharply, the blue cloud-cover curve spikes above 60 %. 
Average daily output:
• Low cloud cover(158days) (≤ 60 %) = 5 000 kWh +
• High cloud cover(145 days) (> 60 %) = 3 000 kWh +

 t-test comparing the two groups: p = 1 × 10⁻¹⁰
 Mean difference = 2 500 kWh
 cloud cover has a very large, significant impact.

**Temperature and Production **
The red temperature curve ranges mostly between 15 °C and 30 °C. Production rises modestly with temperature, but the link is far weaker than for cloud cover.
Using the median temperature (22 °C) as a split:
• Cool days average(152 days) = 4 400 kWh
• Warm days average(151 days) = 4 900 kWh

t-test comparing the two groups: p = 0.02
Mean difference = 500 kWh
Temperature has a smaller effect but still has an impact.

**Model Development(Will be Considered:)**

Selection of appropriate forecasting models and machine learning models.


**This project aims to predict relation between weather conditions and solar panel energy production. The success of this project will contribute to more efficient energy trading and improved operational planning for solar panel energy industry.**



