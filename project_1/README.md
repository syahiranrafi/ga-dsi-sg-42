# ![](https://ga-dash.s3.amazonaws.com/production/assets/logo-9f88ae6c9c3871690e33280fcf557f33.png) Project 1: Data Analysis of Rainfall and Construction Demand in Singapore
Individual submission by Syahiran Rafi

- [Problem Statement](#Problem-Statement) 
- [Data Sets](#Data-Sets)
- [Data Dictionary](#Data-Dictionary)
- [Key Insights](#Key-Insights)
- [Recommendations](#Recommendations)
- [Other Considerations](#Other-Considerations)

### Problem Statement
---
I’m a data analyst working for a company that produces construction materials. The demand for such materials in Singapore often fluctuate during the year. I aim to help my company analyse monthly weather patterns in Singapore to determine if it influences the demand for such materials. The objective is to allow the company to better plan its production capacity and make the necessary price adjustments to sustain demand throughout the year.

### Data Sets
---
The following datasets included in the [`data`](./data/) folder correpond to weather information in Singapore from 1982 to 2022:
* [Total No. of Rain Days per Month](./data/rainfall-monthly-number-of-rain-days.csv)
    -  Monthly number of rain days from 1982 to 2022.
    - A day is considered to have “rained” if the total rainfall for that day is 0.2mm or more.
* [Total Amt of Rainfall per Month](./data/rainfall-monthly-total.csv)
    - Monthly total rain recorded in mm(millimeters) from 1982 to 2022
* [Mean Relative Humidity per Month](https://data.gov.sg/dataset/relative-humidity-monthly-mean)
* [Maximum Daily Rainfall per Month](https://data.gov.sg/dataset/rainfall-monthly-maximum-daily-total)
* [Mean Sunshine Hours per Month](https://data.gov.sg/dataset/sunshine-duration-monthly-mean-daily-duration)
* [Mean Surface Air Temperature per Month](https://data.gov.sg/dataset/surface-air-temperature-mean-daily-minimum)

The following datasets included in the [`data`](./data/) folder correpond to the demand for construction materials in Singapore from 1999 to 2023:
* [Demand for Construction Materials per Month](https://tablebuilder.singstat.gov.sg/table/TS/M400901)


### Data Dictionary
---
|No.|Feature|Type|Dataset|Description|
|---|---|---|---|---|
|1|`month_year`|`str`|rainfall-monthly-number-of-rain-days|YYYY-MM in string format| 
|2|`cement`|`float`|construction-material-demand|Net import of cement in thousand tonnes| 
|3|`steel_bars`|`float`|construction-material-demand|Net import of steel bars in thousand tonnes| 
|4|`granite`|`float`|construction-material-demand|Net import of granite in thousand tonnes| 
|5|`mixed_concrete`|`float`|construction-material-demand|Net import of mixed concrete in thousand cubic metres| 
|6|`total_materials`|`float`|construction-material-demand|Net import of cement, steel bars and granite in thousand tonnes| 
|7|`total_monthly_rainfall`|`float`|rainfall-monthly-total|Total rainfall per month in mm| 
|8|`total_monthly_rain_days`|`int`|rainfall-monthly-number-of-rain-days|Total number of rain days per month (total rainfall exceeds 0.2 mm)| 
|9|`max_daily_rainfall`|`float`|rainfall-monthly-highest-daily-total|Maximum daily rainfall per month in mm| 
|10|`mean_monthly_humidity`|`float`|relative-humidity-monthly-mean|Mean relative humidity per month in %| 
|11|`mean_monthly_sunshine`|`float`|sunshine-duration-monthly-mean-daily-duration|Mean sunshine duration per month in hours| 
|12|`mean_monthly_temp`|`float`|surface-air-temperature-monthly-mean|Mean surface air temperature per month in °C| 
|13|`year`|`str`|rainfall-monthly-number-of-rain-days|YYYY in string format| 
|14|`month`|`str`|rainfall-monthly-number-of-rain-days|MM in string format| 

### Key Insights
---
- Demand for construction materials tends to drop during seasons with extreme weather changes.
- This typically occurs during February (dry weather) and November/December (wet weather).


### Recommendations
---
- Drop in demand is more significant in Q1 (dry weather) than in Q4 (wet weather).
- During the dry season in Q1, adjust price downwards to incentivise buyers and reduce the steep drop in demand.
- During the dry season in Q1, increase production capacity to prepare for the impending demand increase in March, which remains relatively stable thereafter.


### Other Considerations
---
- Changing economic conditions (recession/inflation years) and price fluctuations are generally balanced out by taking the average monthly data from 1999 to 2022 (over 20 years).
- Resource optimisation at the company-level may explain why the demand always drops in the beginning of the year. Companies may prefer to only order supplies/resources in minimum quantities at the start of the year to reduce potential waste.
- Though the construction industry experienced a slump during the peak of the Covid pandemic (2020-2021), it’s showing promising signs of recovery. The Singapore government is also committed to revive the construction industry with various state-level projects, such as:
    - expanding its transport infrastructure (growing the existing and introducing new MRT lines) and
    - meeting the high, pent-up demand for public housing (BTOs)