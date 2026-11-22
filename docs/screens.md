# Screens

Frappe Factory screen designs, built on frappe-ui. Live, clickable version: [Frappe Factory — screens](https://claude.ai/artifact/8NiCgasgTHvjFr3z7civXz). Board sources are in [design/boards](design/boards); the scripts that generate them are in [design/build](design/build).

Production runs, run detail and the Manufacturing half of the Dashboard need ERPNext linked; everything else works standalone. The main story is Koyo 1 at 08:46 on 22 Nov, 32 minutes after the lead interlock tripped. Koyo 1 is the real pilot; every other plant is sample data. The rice mill and oil mill show the same plant screen drawn from other industry symbol packs. Tag addresses and protocols on Devices and tags are sample values until the PLC protocol is chosen.

Every desktop screen uses one Sidebar component. At the top is the app menu (brand and user), opening Apps on this site, Open kiosk, Switch to Desk, help, theme, settings and log out, as in Frappe CRM and Helpdesk. Below it come the company items, or, inside a plant, the plant switcher and plant items. It stays fixed and only scrolls if its own items outgrow the screen; the page body scrolls under a fixed header. Desktop boards are 1440 × 900. Floor kiosks are a 1180 × 820 tablet with no sidebar, by design, in three views: line, maintenance and quality. Every kiosk sign-in is a Frappe user plus that user's PIN.

Units: a sachet is 50 cl and a bag is 20 sachets (10 L). Each Koyo filler is rated at 2,000 sachets (100 bags) an hour, to be confirmed on site. Machine rates and rejects are in sachets, output and plans in bags, and held product in both.

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

## 10 · Quality hold (QA decides held product)

![Quality hold (QA decides held product)](images/screens/10-QualityHold.png)

## 11 · Production runs · needs ERPNext

![Production runs · needs ERPNext](images/screens/11-Runs.png)

## 12 · Run detail · needs ERPNext

![Run detail · needs ERPNext](images/screens/12-RunDetail.png)

## 13 · Downtime

![Downtime](images/screens/13-Downtime.png)

## 14 · Resources

![Resources](images/screens/14-Resources.png)

## 15 · Trends

![Trends](images/screens/15-Trends.png)

## 16 · Shift handover

![Shift handover](images/screens/16-Handover.png)

## 17 · Kiosk · open session

![Kiosk · open session](images/screens/17-KioskOpen.png)

## 18 · Kiosk · sign in with Frappe user + PIN

![Kiosk · sign in with Frappe user + PIN](images/screens/18-KioskLogin.png)

## 19 · Kiosk · line view (filling and packing)

![Kiosk · line view (filling and packing)](images/screens/19-KioskLine.png)

## 20 · Kiosk · maintenance view

![Kiosk · maintenance view](images/screens/20-KioskMaint.png)

## 21 · Kiosk · quality view

![Kiosk · quality view](images/screens/21-KioskQA.png)

## 22 · Plant · Rice mill

![Plant · Rice mill](images/screens/22-RiceMill.png)

## 23 · Plant · Oil mill

![Plant · Oil mill](images/screens/23-OilMill.png)

## 24 · Devices and tags

![Devices and tags](images/screens/24-Devices.png)

## 25 · Layout editor

![Layout editor](images/screens/25-LayoutEditor.png)

## 26 · Symbol library · industry packs

![Symbol library · industry packs](images/screens/26-Symbols.png)

## 27 · Alarm definitions

![Alarm definitions](images/screens/27-AlarmDefs.png)

## 28 · Plant settings · connector

![Plant settings · connector](images/screens/28-Settings.png)

## 29 · Plant settings · commands

![Plant settings · commands](images/screens/29-SettingsCommands.png)
