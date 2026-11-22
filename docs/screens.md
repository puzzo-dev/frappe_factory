# Screens

Frappe Factory screen designs, built on frappe-ui. Live, clickable version: [Frappe Factory — screens](https://claude.ai/artifact/8NiCgasgTHvjFr3z7civXz). Board sources are in [design/boards](design/boards); the scripts that generate them are in [design/build](design/build).

Production runs, run detail and the Manufacturing half of the Dashboard need ERPNext linked; everything else works standalone. The main story is Koyo 1 at 08:46 on 22 Nov, 32 minutes after the lead interlock tripped. Koyo 1 is the real pilot; every other plant is sample data. Plant B (bottled water through ThingsBoard), Plant D (edge offline, last values shown), the rice mill, oil mill and poultry farm show the same plant screen drawn from other industry symbol packs, and each plant has its own layout editor. Every board is linked: the sidebar, app menu, settings navigation, breadcrumbs and kiosk buttons all open the matching board. Tag addresses and protocols on Devices and tags are sample values until the PLC protocol is chosen.

Every desktop screen uses one Sidebar component. At the top is the app menu (brand and user), opening Apps on this site, Open kiosk, Switch to Desk, help, theme, settings and log out, as in Frappe CRM and Helpdesk. Below it come the company items, or, inside a plant, the plant switcher and plant items. It stays fixed and only scrolls if its own items outgrow the screen; the page body scrolls under a fixed header. Desktop boards are 1440 × 900. Floor kiosks are a 1180 × 820 tablet with no sidebar, by design, in three views: line, maintenance and quality. Every kiosk sign-in is a Frappe user plus that user's PIN.

Units: a sachet is 50 cl and a bag is 20 sachets (10 L). Each Koyo filler is rated at 2,000 sachets (100 bags) an hour, to be confirmed on site. Machine rates and rejects are in sachets, output and plans in bags, and held product in both.

### Company

## 0 · Dashboard · factory and manufacturing

![Dashboard · factory and manufacturing](images/screens/00-Dashboard.png)

## 1 · App menu open (apps, Desk, kiosk)

![App menu open (apps, Desk, kiosk)](images/screens/01-DashboardMenu.png)

## 2 · Plants

![Plants](images/screens/02-Plants.png)

## 3 · New plant · choose industry

![New plant · choose industry](images/screens/03-AddPlant.png)

## 4 · My settings · kiosk PIN

![My settings · kiosk PIN](images/screens/04-MySettings.png)

### Across all plants

## 5 · Alarms · all plants

![Alarms · all plants](images/screens/05-CoAlarms.png)

## 6 · Interlock trips · all plants

![Interlock trips · all plants](images/screens/06-CoTrips.png)

## 7 · Production · all plants · needs ERPNext

![Production · all plants · needs ERPNext](images/screens/07-CoProduction.png)

## 8 · Downtime · all plants

![Downtime · all plants](images/screens/08-CoDowntime.png)

## 9 · Quality holds · all plants

![Quality holds · all plants](images/screens/09-CoHolds.png)

## 10 · Maintenance · all plants

![Maintenance · all plants](images/screens/10-CoMaint.png)

## 11 · Reports

![Reports](images/screens/11-CoReports.png)

### Company settings

## 12 · Settings · General

![Settings · General](images/screens/12-CompanyGeneral.png)

## 13 · Settings · Users and roles

![Settings · Users and roles](images/screens/13-CompanyUsers.png)

## 14 · Settings · Kiosks and assigned users

![Settings · Kiosks and assigned users](images/screens/14-CompanyKiosks.png)

## 15 · Settings · Process templates

![Settings · Process templates](images/screens/15-CompanyTemplates.png)

## 16 · Quality hold template editor

![Quality hold template editor](images/screens/16-QHTemplate.png)

## 17 · Settings · ERPNext

![Settings · ERPNext](images/screens/17-CompanyERPNext.png)

## 18 · Settings · API and webhooks

![Settings · API and webhooks](images/screens/18-CompanyAPI.png)

## 19 · Settings · WhatsApp

![Settings · WhatsApp](images/screens/19-CompanyWhatsApp.png)

## 20 · Settings · ThingsBoard

![Settings · ThingsBoard](images/screens/20-CompanyTB.png)

### Inside a plant

## 21 · Plant · Koyo 1 (live)

![Plant · Koyo 1 (live)](images/screens/21-Main.png)

## 22 · Alarms

![Alarms](images/screens/22-Alarms.png)

## 23 · Interlock trips · Koyo 1

![Interlock trips · Koyo 1](images/screens/23-TripList.png)

## 24 · Interlock trip recovery

![Interlock trip recovery](images/screens/24-Trip.png)

## 25 · Quality holds · Koyo 1

![Quality holds · Koyo 1](images/screens/25-HoldList.png)

## 26 · Quality hold (QA decides held product)

![Quality hold (QA decides held product)](images/screens/26-QualityHold.png)

## 27 · Edit pinned tags

![Edit pinned tags](images/screens/27-PinnedTags.png)

### Production

## 28 · Production runs · needs ERPNext

![Production runs · needs ERPNext](images/screens/28-Runs.png)

## 29 · Run detail · needs ERPNext

![Run detail · needs ERPNext](images/screens/29-RunDetail.png)

## 30 · Downtime

![Downtime](images/screens/30-Downtime.png)

## 31 · Resources

![Resources](images/screens/31-Resources.png)

### Analysis and shifts

## 32 · Trends

![Trends](images/screens/32-Trends.png)

## 33 · Shift handover

![Shift handover](images/screens/33-Handover.png)

## 34 · Past shift handovers

![Past shift handovers](images/screens/34-HandoverHistory.png)

### Floor kiosks · full screen like ERPNext POS · line, maintenance and quality views · Frappe user + PIN

## 35 · Kiosk · open session

![Kiosk · open session](images/screens/35-KioskOpen.png)

## 36 · Kiosk · sign in with Frappe user + PIN

![Kiosk · sign in with Frappe user + PIN](images/screens/36-KioskLogin.png)

## 37 · Kiosk · line view (filling and packing)

![Kiosk · line view (filling and packing)](images/screens/37-KioskLine.png)

## 38 · Kiosk · log rejects

![Kiosk · log rejects](images/screens/38-KioskRejects.png)

## 39 · Kiosk · maintenance view

![Kiosk · maintenance view](images/screens/39-KioskMaint.png)

## 40 · Kiosk · report a fault

![Kiosk · report a fault](images/screens/40-KioskFault.png)

## 41 · Kiosk · request a spare part

![Kiosk · request a spare part](images/screens/41-KioskSpare.png)

## 42 · Kiosk · quality view

![Kiosk · quality view](images/screens/42-KioskQA.png)

## 43 · Kiosk · record a sample

![Kiosk · record a sample](images/screens/43-KioskSample.png)

## 44 · Kiosk · decide a held lot

![Kiosk · decide a held lot](images/screens/44-KioskDecide.png)

### Every other plant: bottled water, sachet water offline, rice, oil, poultry

## 45 · Plant · Plant B bottled water (ThingsBoard)

![Plant · Plant B bottled water (ThingsBoard)](images/screens/45-PlantB.png)

## 46 · Plant · Plant D sachet water (offline)

![Plant · Plant D sachet water (offline)](images/screens/46-PlantD.png)

## 47 · Plant · Rice mill

![Plant · Rice mill](images/screens/47-RiceMill.png)

## 48 · Plant · Oil mill

![Plant · Oil mill](images/screens/48-OilMill.png)

## 49 · Plant · Poultry farm (layers)

![Plant · Poultry farm (layers)](images/screens/49-PoultryFarm.png)

### Plant setup · every plant layout is editable

## 50 · Devices and tags

![Devices and tags](images/screens/50-Devices.png)

## 51 · Layout editor · Koyo 1 water

![Layout editor · Koyo 1 water](images/screens/51-LayoutEditor.png)

## 52 · Layout editor · Plant B

![Layout editor · Plant B](images/screens/52-LayoutPlantB.png)

## 53 · Layout editor · Plant D

![Layout editor · Plant D](images/screens/53-LayoutPlantD.png)

## 54 · Layout editor · rice mill

![Layout editor · rice mill](images/screens/54-LayoutRice.png)

## 55 · Layout editor · oil mill

![Layout editor · oil mill](images/screens/55-LayoutOil.png)

## 56 · Layout editor · poultry farm

![Layout editor · poultry farm](images/screens/56-LayoutPoultry.png)

## 57 · Symbol library · industry packs

![Symbol library · industry packs](images/screens/57-Symbols.png)

## 58 · Alarm definitions

![Alarm definitions](images/screens/58-AlarmDefs.png)

## 59 · Plant settings · connector

![Plant settings · connector](images/screens/59-Settings.png)

## 60 · Plant settings · commands

![Plant settings · commands](images/screens/60-SettingsCommands.png)
