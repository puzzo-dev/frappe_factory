# Screens

Frappe Factory screen designs, built on frappe-ui. Live, clickable version: [Frappe Factory — screens](https://claude.ai/artifact/8NiCgasgTHvjFr3z7civXz). Board sources are in [design/boards](design/boards); the scripts that generate them are in [design/build](design/build).

Production runs, run detail and the Manufacturing half of the Dashboard need ERPNext linked; everything else works standalone. The main story is Koyo 1 at 08:46 on 22 Nov, 32 minutes after the lead interlock tripped. Koyo 1 is the real pilot; every other plant is sample data. The rice mill and oil mill show the same plant screen drawn from other industry symbol packs. Tag addresses and protocols on Devices and tags are sample values until the PLC protocol is chosen.

Every desktop screen uses one Sidebar component. At the top is the app menu (brand and user), opening Apps on this site, Open kiosk, Switch to Desk, help, theme, settings and log out, as in Frappe CRM and Helpdesk. Below it come the company items, or, inside a plant, the plant switcher and plant items. It stays fixed and only scrolls if its own items outgrow the screen; the page body scrolls under a fixed header. Desktop boards are 1440 × 900. The floor kiosk is a 1180 × 820 tablet with no sidebar, by design.

## 0 · Dashboard · factory and manufacturing

![Dashboard · factory and manufacturing](images/screens/00-Dashboard.png)

## 1 · App menu open (apps, Desk, kiosk)

![App menu open (apps, Desk, kiosk)](images/screens/01-DashboardMenu.png)

## 2 · Plants

![Plants](images/screens/02-Plants.png)

## 3 · New plant · choose industry

![New plant · choose industry](images/screens/03-AddPlant.png)

## 4 · Settings · ERPNext

![Settings · ERPNext](images/screens/04-CompanyERPNext.png)

## 5 · Settings · API and webhooks

![Settings · API and webhooks](images/screens/05-CompanyAPI.png)

## 6 · Settings · Kiosks and assigned users

![Settings · Kiosks and assigned users](images/screens/06-CompanyKiosks.png)

## 7 · Plant · Koyo 1 (live)

![Plant · Koyo 1 (live)](images/screens/07-Main.png)

## 8 · Alarms

![Alarms](images/screens/08-Alarms.png)

## 9 · Interlock trip recovery

![Interlock trip recovery](images/screens/09-Trip.png)

## 10 · Production runs · needs ERPNext

![Production runs · needs ERPNext](images/screens/10-Runs.png)

## 11 · Run detail · needs ERPNext

![Run detail · needs ERPNext](images/screens/11-RunDetail.png)

## 12 · Downtime

![Downtime](images/screens/12-Downtime.png)

## 13 · Resources

![Resources](images/screens/13-Resources.png)

## 14 · Trends

![Trends](images/screens/14-Trends.png)

## 15 · Shift handover

![Shift handover](images/screens/15-Handover.png)

## 16 · Kiosk · open session

![Kiosk · open session](images/screens/16-KioskOpen.png)

## 17 · Kiosk · sign in (assigned users only)

![Kiosk · sign in (assigned users only)](images/screens/17-KioskLogin.png)

## 18 · Kiosk · line view

![Kiosk · line view](images/screens/18-KioskLine.png)

## 19 · Plant · Rice mill

![Plant · Rice mill](images/screens/19-RiceMill.png)

## 20 · Plant · Oil mill

![Plant · Oil mill](images/screens/20-OilMill.png)

## 21 · Devices and tags

![Devices and tags](images/screens/21-Devices.png)

## 22 · Layout editor

![Layout editor](images/screens/22-LayoutEditor.png)

## 23 · Symbol library · industry packs

![Symbol library · industry packs](images/screens/23-Symbols.png)

## 24 · Alarm definitions

![Alarm definitions](images/screens/24-AlarmDefs.png)

## 25 · Plant settings · connector

![Plant settings · connector](images/screens/25-Settings.png)

## 26 · Plant settings · commands

![Plant settings · commands](images/screens/26-SettingsCommands.png)
