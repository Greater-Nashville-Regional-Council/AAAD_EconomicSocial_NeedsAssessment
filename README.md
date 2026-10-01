# AAAD_EconomicSocial_NeedsAssessment
Repository hosting economic and social needs assessment files for the AAAD.


As part of the Aging Area Plan, the state is now requiring us to identify the populations in our region who are in greatest economic need and the populations who are in greatest social need. Below are the state’s definitions of these terms. This is an addition to area plan that’s updated every year – aligned with new Older American’s Act.
 

Definitions:   
+ Greatest Economic Need: the need resulting from an income level at or below the Federal poverty level and as further defined by State and area plans based on local and individual factors, including geography and expenses.
 
 
+ Greatest Social Need: the need caused by noneconomic factors, which include:  
              (1) Physical and mental disabilities;  
              (2) Language barriers;  
              (3) Cultural, social, or geographical isolation, including due to: Racial or ethnic status; Native American identity; Religious affiliation; Sexual orientation, gender identity, or sex characteristics; HIV status; Housing instability, food insecurity, lack of access to reliable and clean water supply, lack of transportation, or utility assistance needs; Interpersonal safety concerns; Rural location; or Any other status that: Restricts the ability of an individual to perform normal or routine daily tasks; or threatens the capacity of the individual to live independently; or other needs as further defined by State and area plans based on local and individual factors.  

Question: Do we have this (or similar) data available that we can use to identify cities or zip codes that would have the highest population of individuals who fit these definitions?  

Approach: Source data for best fit that is available uniformly, create an index to identify critical areas.

Index Methodology:

# Economic and Social Needs Index

## Overview

The Needs Index identifies ZIP Code Tabulation Areas (ZCTAs) with relatively high levels of economic and social need. The methodology evaluates a set of economic and social indicators, standardizes each indicator relative to the study area, and combines the resulting rankings into separate Economic Need and Social Need measures.

A ZCTA is identified as having combined economic and social need when it meets the high-need threshold for **both** components.

The index is intended as a relative measure of need within the selected study area rather than an absolute threshold for economic or social hardship.

## Geography

The analysis is conducted at the **ZIP Code Tabulation Area (ZCTA)** level.

Because ZCTAs are not nested cleanly within counties or other Census geographies, the study-area ZCTAs are identified using a list of ZCTAs hand-selected through MySidewalk's user portal. This list is then used to filter the Census data to the geography included in the analysis.

## Data Sources

The index uses the following sources of data, vintages, and methods of pulling:

**U.S. Census Bureau, 2020–2024 American Community Survey 5-Year Estimates**

Census data provide the demographic, socioeconomic, housing, and transportation indicators used in the Economic and Social Need components. Via internal ETL pipeline. 2020-2024.

**Federal Emergency Management Agency**  

FEMA data provide environmental hazard expected annual loss of population. Via MySidewalk. 2025.

**Environmental Protection Agency**

EPA data provide the diesel particulate matter level in the air (2024) and drinking water non-compliance (2024) - both part of EJSCREEN. Via MySidewalk.  

**Federal Office of Rural Health Policy**

FORHP data provide rural area. Via MySidewalk. 2025.

**US Department of Agriculture**  

USDA ERS (Economic Research Service) data provide the people by urban/rural distance with low access to healthy food. Via MySidewalk. 2025.

## Economic Need

The Economic Need component consists of three indicators:

| Indicator | Description | Census Detailed Tables Series Variable
| --- | --- | --- |
| `EC_POV` | Population below the poverty level | B17001
| `EC_CB` | Cost-burdened households | B25070, B25091
| `EC_UNEMP` | Unemployed civilian population | B23001  

### Indicator Classification

Each indicator is evaluated relative to its distribution across the study area.

For each indicator, a **population-weighted mean and population-weighted standard deviation** are calculated using ACS population as the weight.

For indicator \(x\) and population weight \(w\):

The population-weighted mean is calculated as:

weighted mean = sum(population × indicator value) / sum(population)

The population-weighted standard deviation is calculated as:

weighted standard deviation = sqrt[sum(population × (indicator value - weighted mean)²) / sum(population)]  

Each ZCTA is then assigned a rank from 0 to 4 based on how its indicator value compares with the weighted mean and standard deviation:

Rank

Category

Classification

0

Well below average

Value < mean − 2 standard deviations

1

Below average

Mean − 2 standard deviations ≤ value < mean − 1 standard deviation

2

Average

Mean − 1 standard deviation ≤ value ≤ mean + 1 standard deviation

3

Above average

Mean + 1 standard deviation < value ≤ mean + 2 standard deviations

4

Well above average

Value > mean + 2 standard deviations

Missing indicator rankings are assigned a value of **2**, representing the neutral category.

### Economic Composite Score

The three economic indicator rankings are summed:

SUM_EC = EC_POV_R + EC_CB_R + EC_UNEMP_R

Higher values therefore represent greater cumulative economic need.

### Economic Need Designation

The 60th percentile of `SUM_EC` is calculated across ZCTAs in the analysis.

A ZCTA is classified as having Economic Need when:

SUM_EC > 60th percentile of SUM_EC

The resulting binary variable is:

- `EC_NEED = 1`: Economic Need
- `EC_NEED = 0`: Not classified as Economic Need

Conceptually, this identifies ZCTAs falling above the cutoff used to represent approximately the **highest 40 percent of composite economic scores**. Because the code uses a strict greater-than (`>`) comparison, ties at the 60th-percentile value are not classified as Economic Need; therefore, exactly 40 percent of ZCTAs are not guaranteed to receive the designation.

## Social Need

The Social Need component consists of ten indicators covering demographic vulnerability, transportation access, environmental conditions, rural status, and food access.

| Indicator | Description | Source/Census Detailed Tables Series Variable
| --- | --- | --- |
| `SC_AGE65` | Population age 65 and older | B01001  
| `SC_MIN` | Minority population | B01001A-I  
| `SC_DISABL` | Population with a disability | B18101  
| `SC_LIMENG` | Population speaking English not well or not at all | B16004  
| `SC_NOVEH` | Households with no vehicle available | B25044  
| `SC_ENVHAZL` | Environmental hazard expected annual loss | EPA NRI  
| `SC_DPML` | Diesel particulate matter level in air | EPA EJSCREEN  
| `SC_WATER` | Drinking water non-compliance | EPA EJSCREEN  
| `SC_RURAL` | Federal Office of Rural Health Policy rural-area indicator | FORHP  
| `SC_FOOD` | Population with low access to healthy food, defined using the 1-mile urban/10-mile rural measure | USDA ERS  

### Indicator Classification

The same procedure used for the Economic Need indicators is applied to each Social Need indicator.

For each variable:

1. A population-weighted mean is calculated.
2. A population-weighted standard deviation is calculated.
3. Each ZCTA is categorized relative to those values using the project's `categorize()` function.
4. Missing rankings are assigned the neutral value of **2**.

Population from the ACS is used as the weight for all ten indicators.

### Social Composite Score

The ten Social Need indicator rankings are summed to create the Social Need composite score:

SUM_SC = SC_AGE65_R + SC_MIN_R + SC_DISABL_R + SC_LIMENG_R + SC_NOVEH_R + SC_ENVHAZL_R + SC_DPML_R + SC_WATER_R + SC_RURAL_R + SC_FOOD_R

Because each of the ten indicators can receive a rank from 0 to 4, SUM_SC can theoretically range from 0 to 40.

Higher scores represent a greater accumulation of social-need characteristics.

### Social Need Designation

The 60th percentile of `SUM_SC` is calculated.

A ZCTA is classified as having Social Need when:

SUM_SC > 60th percentile of SUM_SC

The resulting binary variable is:

- `SC_NEED = 1`: Social Need
- `SC_NEED = 0`: Not classified as Social Need

As with Economic Need, the strict greater-than comparison means the final share classified as Social Need may be less than 40 percent when ZCTAs share the threshold score.

## Combined Economic and Social Need

The Economic Need and Social Need results are joined by ZCTA, name, and population.

A final combined indicator, `EC_SC_NEED`, identifies ZCTAs that meet **both** criteria:

EC_SC_NEED = 1 if EC_NEED = 1 AND SC_NEED = 1; otherwise EC_SC_NEED = 0

Therefore, the combined designation is an **intersection rather than an additive score**. A ZCTA with high Social Need but not high Economic Need, or vice versa, is not classified as having combined need.

Methodological Interpretation

Several aspects of the methodology are important when interpreting the results.

Relative rather than absolute need. The index measures conditions relative to other ZCTAs in the selected study area. A ZCTA's classification can therefore change if the study geography changes, even if the ZCTA's underlying conditions remain the same.

Population-weighted benchmarks. The mean and standard deviation used to classify each indicator are weighted by ACS population. More populous ZCTAs therefore have greater influence on the benchmarks used to determine what constitutes average, above-average, or below-average conditions.

Standardized categorical rankings. Indicators measured in different units are converted to a common 0–4 ranking before being combined. This allows percentages, counts, environmental measures, and other indicators to contribute to the same composite index without directly adding their original values.

Equal contribution within components. Once standardized, indicator rankings are summed without additional indicator-specific weights. Each indicator therefore has the same possible contribution—0 through 4 points—to its respective composite score.

Neutral treatment of missing values. Missing indicator rankings are assigned a value of 2, equivalent to the average category, rather than being excluded from the composite calculation.

Distribution-based need threshold. Economic and Social Need designations are based on the distribution of composite scores within the study area rather than an externally defined hardship threshold. ZCTAs with scores above the 60th percentile are designated as having need for that component.

Combined need is intentionally restrictive. The final combined measure requires a ZCTA to meet the high-need threshold for both the Economic and Social Need components.

Workflow Summary

The methodology consists of the following steps:

Retrieve ACS 2020–2024 5-year data at the ZCTA level.

Merge the required ACS Detailed Tables.

Identify ZCTAs within the study area using the MySidewalk geography selection.

Assemble the three Economic Need indicators.

Calculate population-weighted means and standard deviations for each indicator.

Assign each indicator a 0–4 ranking based on its distance from the weighted mean.

Sum the Economic Need rankings to create SUM_EC.

Identify ZCTAs with SUM_EC values above the 60th percentile and assign EC_NEED.

Assemble the ten Social Need indicators from ACS and external sources.

Calculate population-weighted means and standard deviations for each Social Need indicator.

Assign each indicator a 0–4 ranking.

Sum the Social Need rankings to create SUM_SC.

Identify ZCTAs with SUM_SC values above the 60th percentile and assign SC_NEED.

Combine the Economic and Social Need results.

Assign EC_SC_NEED = 1 to ZCTAs meeting both need criteria.

Output Variables

Variable

Description

SUM_EC

Sum of the three Economic Need indicator rankings; theoretical range 0–12

EC_NEED

Binary Economic Need designation

SUM_SC

Sum of the ten Social Need indicator rankings; theoretical range 0–40

SC_NEED

Binary Social Need designation

EC_SC_NEED

Binary designation identifying ZCTAs classified as both Economic Need and Social Need
