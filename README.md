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

A ZCTA is ultimately identified as having combined economic and social need when it meets the high-need threshold for **both** components.

The index is intended as a relative measure of need within the selected study area. It does not represent an absolute threshold for economic or social hardship.

## Geography

The analysis is conducted at the **ZIP Code Tabulation Area (ZCTA)** level.

ZCTA identifiers are derived from the final five characters of the Census `GEO_ID` field.

Because ZCTAs are not nested cleanly within counties or other Census geographies, the study-area ZCTAs are identified using a list of ZCTAs selected through MySidewalk. This list is then used to filter the Census data to the geography included in the analysis.

## Data Sources

The index uses three primary groups of data:

**U.S. Census Bureau, 2020–2024 American Community Survey 5-Year Estimates**

Census data provide the demographic, socioeconomic, housing, and transportation indicators used in the Economic and Social Need components.

**MySidewalk**

A MySidewalk download provides the ZCTAs defining the study area as well as several environmental, rural-access, and food-access indicators derived from external federal datasets.

These external indicators include data originating from the U.S. Environmental Protection Agency (EPA) and U.S. Department of Agriculture (USDA).

## Economic Need

The Economic Need component consists of three indicators:

| Indicator | Description |
| --- | --- |
| `EC_POV` | Population below the poverty level |
| `EC_CB` | Cost-burdened households |
| `EC_UNEMP` | Unemployed civilian population |

### Indicator Classification

Each indicator is evaluated relative to its distribution across the study area.

For each indicator, a **population-weighted mean and population-weighted standard deviation** are calculated using ACS population as the weight.

For indicator \(x\) and population weight \(w\):

**Weighted mean**

\[
\bar{x}_w = \frac{\sum w_i x_i}{\sum w_i}
\]

**Weighted standard deviation**

\[
\sigma_w =
\sqrt{
\frac{\sum w_i(x_i-\bar{x}_w)^2}
{\sum w_i}
}
\]

Each ZCTA's indicator value is then assigned a categorical rank based on its position relative to the weighted mean and standard deviation.

> **Methodology note:** The precise category thresholds and rank values are defined in the project's `categorize()` function in `src.functions` and should be documented here from that function.

Missing indicator rankings are assigned a value of **2**, representing the neutral category.

### Economic Composite Score

The three economic indicator rankings are summed:

\[
SUM\_EC =
EC\_POV\_R +
EC\_CB\_R +
EC\_UNEMP\_R
\]

Higher values therefore represent greater cumulative economic need.

### Economic Need Designation

The 60th percentile of `SUM_EC` is calculated across ZCTAs in the analysis.

A ZCTA is classified as having Economic Need when:

\[
SUM\_EC > P_{60}(SUM\_EC)
\]

The resulting binary variable is:

- `EC_NEED = 1`: Economic Need
- `EC_NEED = 0`: Not classified as Economic Need

Conceptually, this identifies ZCTAs falling above the cutoff used to represent approximately the **highest 40 percent of composite economic scores**. Because the code uses a strict greater-than (`>`) comparison, ties at the 60th-percentile value are not classified as Economic Need; therefore, exactly 40 percent of ZCTAs are not guaranteed to receive the designation.

## Social Need

The Social Need component consists of ten indicators covering demographic vulnerability, transportation access, environmental conditions, rural status, and food access.

| Indicator | Description |
| --- | --- |
| `SC_AGE65` | Population age 65 and older |
| `SC_MIN` | Minority population |
| `SC_DISABL` | Population with a disability |
| `SC_LIMENG` | Population speaking English not well or not at all |
| `SC_NOVEH` | Households with no vehicle available |
| `SC_ENVHAZL` | Environmental hazard expected annual loss |
| `SC_DPML` | Diesel particulate matter level in air |
| `SC_WATER` | Drinking water non-compliance |
| `SC_RURAL` | Federal Office of Rural Health Policy rural-area indicator |
| `SC_FOOD` | Population with low access to healthy food, defined using the 1-mile urban/10-mile rural measure |

### Indicator Classification

The same procedure used for the Economic Need indicators is applied to each Social Need indicator.

For each variable:

1. A population-weighted mean is calculated.
2. A population-weighted standard deviation is calculated.
3. Each ZCTA is categorized relative to those values using the project's `categorize()` function.
4. Missing rankings are assigned the neutral value of **2**.

Population from the ACS is used as the weight for all ten indicators.

### Social Composite Score

The ten social indicator rankings are summed:

\[
\begin{aligned}
SUM\_SC ={}&
SC\_AGE65\_R +
SC\_MIN\_R +
SC\_DISABL\_R +\\
&SC\_LIMENG\_R +
SC\_NOVEH\_R +
SC\_ENVHAZL\_R +\\
&SC\_DPML\_R +
SC\_WATER\_R +
SC\_RURAL\_R +
SC\_FOOD\_R
\end{aligned}
\]

Higher scores represent a greater accumulation of social-need characteristics.

### Social Need Designation

The 60th percentile of `SUM_SC` is calculated.

A ZCTA is classified as having Social Need when:

\[
SUM\_SC > P_{60}(SUM\_SC)
\]

The resulting binary variable is:

- `SC_NEED = 1`: Social Need
- `SC_NEED = 0`: Not classified as Social Need

As with Economic Need, the strict greater-than comparison means the final share classified as Social Need may be less than 40 percent when ZCTAs share the threshold score.

## Combined Economic and Social Need

The Economic Need and Social Need results are joined by ZCTA, name, and population.

A final combined indicator, `EC_SC_NEED`, identifies ZCTAs that meet **both** criteria:

\[
EC\_SC\_NEED =
\begin{cases}
1, & EC\_NEED = 1 \text{ and } SC\_NEED = 1\\
0, & \text{otherwise}
\end{cases}
\]

Therefore, the combined designation is an **intersection rather than an additive score**. A ZCTA with high Social Need but not high Economic Need, or vice versa, is not classified as having combined need.

## Methodological Interpretation

Several
