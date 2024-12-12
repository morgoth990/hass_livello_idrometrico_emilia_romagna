# Livello idrometrico Emilia Romagna
This integration reads data from the [official website of Emilia Romagna](https://allertameteo.regione.emilia-romagna.it/livello-idrometrico) and can be used to create one or more Devices representing the measuring stations of the hydrometric level of rivers.

## Configuration
This integration can be installed by adding the repository url via Hacs.
Subsequently, from the integrations menu, you can add a new device by selecting the desired station from the drop-down menu:

<img width="331" alt="image" src="https://github.com/user-attachments/assets/38c21a94-00f1-467b-80af-d4922c17c597" />


## Usage
Each added station will create a device with the same name:

<img width="377" alt="image" src="https://github.com/user-attachments/assets/d6f34977-01de-4837-b935-7b19945b0343" />

The possible value of the Alert sensor are: Unknown, None, Yellow, Orange, Red

I recommend using ApexCharts to show the values ​​chart so you can set the correct colors for the thresholds and specify the minimum and maximum value on the y-axis:

<img width="359" alt="image" src="https://github.com/user-attachments/assets/c01532a4-3346-473c-877a-76b1a2a0ece5" />

(Remember to set the min and max values ​​according to the station range)

```yaml
type: custom:apexcharts-card
graph_span: 24h
yaxis:
  - opposite: true
    min: 8
    max: 12
header:
  show: false
  show_states: false
  colorize_states: false
apex_config:
  grid:
    show: false
  xaxis:
    axisBorder:
      show: false
    axisTicks:
      show: false
    tooltip:
      enabled: false
  chart:
    offsetY: 0
  legend:
    show: false
series:
  - entity: sensor.lavino_di_sopra_theshold_3_red
    type: line
    color: red
    stroke_width: 1
    stroke_dash: 5
  - entity: sensor.lavino_di_sopra_theshold_2_orange
    type: line
    color: orange
    stroke_width: 1
    stroke_dash: 5
  - entity: sensor.lavino_di_sopra_theshold_1_yellow
    type: line
    color: yellow
    stroke_width: 1
    stroke_dash: 5
  - entity: sensor.lavino_di_sopra_water_level
    type: area
    color: steelblue
    stroke_width: 4
    opacity: 0.5

```

