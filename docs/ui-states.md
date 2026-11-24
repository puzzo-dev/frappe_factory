# UI states

The states each flow can be in, beyond the main screens. Each one is a board on the design canvas (`docs/design/boards/<Name>.dc.html`), built by `docs/design/build/s_states.py` from its base screen. From the 23 Nov 2026 UI review (Frappe `ui-design` and `review-ui-states`).

## Kiosk session

| Board | State |
| --- | --- |
| `KioskLocked` | Five wrong PINs lock that user on every kiosk at the plant for 15 min. |
| `KioskFirstSignIn` | First sign-in on a kiosk: Frappe login (online), then choose a PIN. Repeated every 7 days. |
| `KioskIdle` | After 9.5 min without a tap the kiosk warns, then logs out at 10 min. |
| `KioskOffline` | Cloud setup with the internet down: values freeze, saves queue on the tablet. |
| `KioskSaveRetry` | A save that fails keeps the entry and retries; the button shows the attempt. |
| `KioskClosing` | Closing the kiosk session: a supervisor reviews the shift totals and open items. |

## Alarm lifecycle

| Board | State |
| --- | --- |
| `AlarmsCleared` | A cleared alarm nobody acknowledged stays listed and keeps escalating. |
| `AlarmsShelved` | Shelved alarms with who shelved them, why, and until when. |
| `AlarmsHistory` | Closed alarms with how long they took to acknowledge. |
| `AlarmsEscalated` | An unacknowledged alarm past its response time goes up a level. |
| `AlarmsFlood` | A flood: downstream alarms are held under the trip so the four that matter stay visible. |
| `AlarmsNone` | The calm state: no active alarms, with the last one named. |

## Plant monitoring

| Board | State |
| --- | --- |
| `PlantConnecting` | A newly paired plant before its first message: nothing is shown as a value. |
| `PlantDelayed` | Between live and offline: data 30 s to 5 min old, shown as delayed. |
| `PlantNoLayout` | A plant with tags but no layout: live values elsewhere work, the layout area invites one. |

## Trip recovery

| Board | State |
| --- | --- |
| `TripAwaitingRelease` | Both samples passed; only the Quality Inspector can release the line. |
| `TripAwaitingReset` | QA released; the PLC interlock is reset only by the key at the panel. |
| `TripRestarted` | Restarted after the key reset; the trip closes with its quality hold. |
| `TripSampleFailed` | A failed release sample sends recovery back to sampling. |

## Quality hold

| Board | State |
| --- | --- |
| `HoldReadyClose` | Every lot decided: the hold can be closed and its stock moves posted. |
| `HoldClosed` | A closed hold shows what was posted and closes its trip. |
| `HoldDeviation` | A release with deviation waits for a second person, the Factory Manager. |
| `HoldPostFailed` | If ERPNext refuses a stock move, the hold stays open and says why. |

## Downtime reason

| Board | State |
| --- | --- |
| `DowntimeSaved` | After picking a reason: the row updates and a short confirmation shows. |
| `DowntimeAllGiven` | Every stop today has a reason: the badge says so instead of disappearing. |

## Production run

| Board | State |
| --- | --- |
| `RunStart` | Start a run from a work order; it stays disabled while a hold blocks it. |
| `RunEndConfirm` | Ending a run shows what will post to ERPNext before it does. |
| `RunPostFailed` | Ended but not posted: counts are kept and the ERPNext error is shown. |
| `RunNoERPNext` | The same run with ERPNext off: no work order, nothing posted. |

## Shift handover

| Board | State |
| --- | --- |
| `HandoverSubmitted` | Submitted and waiting for the incoming supervisor to accept. |
| `HandoverAccepted` | Accepted: the shift closes and the handover becomes read-only. |
| `HandoverBlocked` | Without a submitted handover the shift cannot close. |

## Layout editor

| Board | State |
| --- | --- |
| `LayoutEmpty` | A new layout: start from the Process Flow or by dragging symbols. |
| `LayoutFromFlow` | Generated from the Process Flow; a notice says what was placed and what to check. |
| `LayoutPreview` | Preview shows the draft as operators will see it, with live values, before publishing. |
| `LayoutPublishConfirm` | Publishing shows what changed and any problems left. |
| `LayoutPublished` | Published: the version is live and the previous one is kept. |
| `LayoutConflict` | Two people editing: the second publisher merges or saves a new version. |

## Process flow

| Board | State |
| --- | --- |
| `FlowProposing` | Roles below Factory Manager propose a change through the workflow. |
| `FlowRejected` | A rejected proposal keeps the reason and leaves the live version unchanged. |
| `FlowReadOnly` | With no workflow for their role, lower roles can only read the flow. |
| `FlowDeadEnd` | Validation blocks approval while any path ends without a filler, drain or return. |

## Add plant

| Board | State |
| --- | --- |
| `AddPlantDetails` | Step 1: the plant's name, code, place and warehouse. |
| `AddPlantEdge` | Step 3: pair the plant's edge box with a code. |
| `AddPlantLayout` | Step 4: the first layout, from the template, another plant or blank. |
| `AddPlantDone` | Finished: what was created and what happens next. |

## Resources and power

| Board | State |
| --- | --- |
| `ResourcesGrid` | The grid is back: the switch is read from ATS-1 and the generator stops. |
| `ResourcesNotMeasured` | Without an ATS, controller or meter signal, the source is shown as not measured. |
| `ResourcesDieselLow` | Diesel under its reorder point, with the request already raised. |

## Connector

| Board | State |
| --- | --- |
| `ConnTestFailed` | Test now fails: the message says which side did not answer. |
| `ConnUplinkDown` | The uplink is down: the buffer fills on the box and screens say how old the data is. |
| `ConnCodeExpired` | An unused pairing code expires after 24 h; a new one is one click. |
| `ConnUnsaved` | A changed field shows a save bar; closing asks before discarding. |

## Edge box

| Board | State |
| --- | --- |
| `EdgeUplinkDown` | Uplink down on the box itself: the buffer grows, local work carries on. |
| `EdgeClockUnsynced` | With the clock unsynced the box keeps reading but holds uploads. |
| `EdgeUnpaired` | First boot: the only job is to enter the pairing code. |
| `EdgeUpdating` | An update in progress, with the automatic rollback stated. |
| `EdgeDeviceOffline` | One device stops answering: which port, since when, and what still works. |
| `EdgeScanEmpty` | A scan that finds nothing says what it tried and what to check. |
| `EdgeLocked` | Local logins lock after five wrong passwords, with the way to reset on the box. |

## Devices and tags

| Board | State |
| --- | --- |
| `DevicesOffline` | A device that stops answering marks its tags Bad and points to the edge page. |
| `DevicesBadTag` | A value outside the sensor range is marked Bad and pauses its alarms. |
| `DevicesSuggestions` | Devices the edge box found arrive as suggestions to review. |
| `DevicesConfigHistory` | The history of config versions sent to the box, with restore. |

## Company lists

| Board | State |
| --- | --- |
| `ListLoading` | Loading: rows keep their shape so nothing jumps when data arrives. |
| `ListEmpty` | Empty: says the plants are reporting, so empty means calm, not broken. |
| `ListNoResults` | No results for a search or filter, with a way out. |
| `ListFailed` | A failed load says what failed and that alarms are still being raised. |
| `SettingsPlantSite` | Connector with deployment 2 chosen: plant site address, sync, what it holds and never holds, who can use it. |
| `SettingsSyncProblem` | Deployment 2: a record the cloud rejected is kept, shown with its reason, fixed and resent with the same number. |
