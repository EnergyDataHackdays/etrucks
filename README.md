# FIT4Grid - Future Integration of logistics E-Trucks in Grid design and operation

## Name
FIT4Grid - Future Integration of logistics E-Trucks in Grid design and operation

## Description
Git repo to track the development of the FIT4Grid project

## Data
Under the directory `data` you should place the data used in the project.

- `data/`


## Data explanations
The columns of 'StrategischerTourenplan_HSLU.xlsx' are explained as follows:
- **Wochentag**: Day of the week
- **Tournummer**: Tour number 
- **Tourtyp**: Tourtyp
- **SAP**: SAP number of the location
- **VST**: Verkaufsstelle = Filiale
- **Ladefolge**: Loading sequence
- **Sort:** Sortiment
- **Abfahrtszeit Beladestelle**: Departure time Hub
- **Anlieferzeit**: Arrival time at location
- **Tourendzeit**: Tour end time
- **Motorwagen/Anhänger:** Truck/Trailer H: Trailer, M: Truck
- **LKW-Kapazität**: Truck capacity (number of "Rollbehälter")
- **Einheiten**: Number of units per category

The columns of 'Filial_Master_NWZZ.xlsx' are explained as follows:

- **Typ**: Type of location
- **VST-Nummer**: Verkaufsstelle number (corresponds to SAP number in 'StrategischerTourenplan_HSLU.xlsx')
- **Format**: Format of the location
- **Name**: Name of the location
- **Strasse**: Street of the location
- **PLZ**: Postal code of the location
- **Stadt**: City of the location

## Tasks

- [ ] Obtain and explore the data folder
- [ ] Parse and explore the data
- [ ] Perform simple analytics based on the data
- [ ] Create visualization of the data
- [ ] Map routes on a map including information (see example scripts)
- [ ] Create 'availability', 'vehicletype' and 'vehicle_mapping' file for further processing (example file see `/templates`)
- [ ] Explore various smart charging approaches based on the e-truck fleets in terms of peak consumption required, energy costs, etc.



## Code
There are multiple [jupyter notebooks](https://jupyter.org/) in the repo:
- [Coords_and_missing_addresses_to_locations.ipynb](Coords_and_missing_addresses_to_locations.ipynb) : Cleans the `Filial_Master_NWZZ.xlsx` by adding missing data and providing geocoordinates. The result is saved to `data/locations_with_coords.xlsx`.
- [daily_total_distance.ipynb](daily_total_distance.ipynb): Sums the total expected distance and driving duration of the whole fleet from `data/routes_with_distance.xlsx`.
- [fleet_analytics.ipynb](fleet_analytics.ipynb): Initial script to familiarize with data.
- [route_distance.ipynb](route_distance.ipynb): Calculates the distance of each route using `data/locations_with_coords.xlsx`, `data/StrategischerTourenplan_HSLU.xlsx` and a local [Openroute](https://openrouteservice.org/) server and saves it to `data/routes_with_distance.xlsx`.
- [data/routes_with_distance.xlsx](data/routes_with_distance.xlsx): Creates histograms to present the distances the fleet travels using `data/routes_with_distance.xlsx`.
- [route_plot_spider.ipynb](route_plot_spider.ipynb): Creates map visualizations of the most frequently used routes using `data/routes_with_distance.xlsx`.
- [time_histograms.ipynb](time_histograms.ipynb): Uses `data/routes_with_distance.xlsx` to create histograms of departure and arrival times of the fleet.