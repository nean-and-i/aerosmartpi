# aerosmartpi
Raspberry Pi based monitoring solution for Aerosmart devices of Drexel und Weiss


## Features:

- Open source based visualization and monitoring of Aerosmart devices
- web based Interface (plattform idependent: mac, pc, tablet, smartphone,… )
- minimal costs due to use of embedded Linux  <50EUR!! (prototype runs on Raspberry PI)
- no additional adaption or development required on Aerosmat devises
- security concept; modular architecture, no access and no feedback to Aerosmart
	- write acces impossible, decoupled 
	- restrictive error handling 
- full monitoring via munin
- fhem integration (backwardcompatibility to legacy bussystem eg. KNX, Onewire, etc.)
- sync to cloud, acces from averywhere
- alarming via mail, triggered by any parameter
- remote access for support via openvpn

### possible scenarios / follow up development
- native IOS and Android app
   - read access / write access possible with permission of the vendor
- integration into common future home automation IoT
	- Google Nest API
	- Apple Homekit 
	- smartvisu
 
 
 


## Screenshots

![](/images/AerosmartPI.png)


