# Screens

Frappe Factory screen designs, built on frappe-ui. Live, clickable version: [Frappe Factory — screens](https://claude.ai/artifact/8NiCgasgTHvjFr3z7civXz). Board sources are in [design/boards](design/boards); the scripts that generate them are in [design/build](design/build).

The main story is Koyo 1 at 08:46 on 22 Nov, 32 minutes after the lead interlock tripped. Koyo 1 is the real pilot; every other plant is sample data. The rice mill and oil mill show the same plant screen drawn from other industry symbol packs. Tag addresses and protocols on Devices and tags are sample values until the PLC protocol is chosen.

Every desktop screen uses one Sidebar component: the company version on Plants and New plant, the plant version inside a plant. It stays fixed and only scrolls if its own items outgrow the screen; the page body scrolls under a fixed header. Desktop boards are 1440 × 900. The floor kiosk is a 1180 × 820 tablet with no sidebar, by design.

## 0 · Plants (home)

![Plants (home)](images/screens/00-Plants.png)

## 1 · New plant · choose industry

![New plant · choose industry](images/screens/01-AddPlant.png)

## 2 · Plant · Koyo 1 (live)

![Plant · Koyo 1 (live)](images/screens/02-Main.png)

## 3 · Alarms

![Alarms](images/screens/03-Alarms.png)

## 4 · Interlock trip recovery

![Interlock trip recovery](images/screens/04-Trip.png)

## 5 · Production runs

![Production runs](images/screens/05-Runs.png)

## 6 · Run detail

![Run detail](images/screens/06-RunDetail.png)

## 7 · Downtime

![Downtime](images/screens/07-Downtime.png)

## 8 · Resources

![Resources](images/screens/08-Resources.png)

## 9 · Trends

![Trends](images/screens/09-Trends.png)

## 10 · Shift handover

![Shift handover](images/screens/10-Handover.png)

## 11 · Kiosk · sign in with PIN

![Kiosk · sign in with PIN](images/screens/11-KioskLogin.png)

## 12 · Kiosk · line view

![Kiosk · line view](images/screens/12-KioskLine.png)

## 13 · Plant · Rice mill

![Plant · Rice mill](images/screens/13-RiceMill.png)

## 14 · Plant · Oil mill

![Plant · Oil mill](images/screens/14-OilMill.png)

## 15 · Devices and tags

![Devices and tags](images/screens/15-Devices.png)

## 16 · Layout editor

![Layout editor](images/screens/16-LayoutEditor.png)

## 17 · Symbol library · industry packs

![Symbol library · industry packs](images/screens/17-Symbols.png)

## 18 · Alarm definitions

![Alarm definitions](images/screens/18-AlarmDefs.png)

## 19 · Plant settings · connector

![Plant settings · connector](images/screens/19-Settings.png)

## 20 · Plant settings · commands

![Plant settings · commands](images/screens/20-SettingsCommands.png)
