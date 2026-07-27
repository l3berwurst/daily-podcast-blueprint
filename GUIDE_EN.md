# English Step-by-Step Guide
## Daily Podcast on a Media Player – Version 6.4

This guide explains the complete installation, configuration, operation, testing, and troubleshooting of the **“Daily Podcast on a Media Player – Version 6.4”** Home Assistant Blueprint.

The Blueprint uses a Pyscript service to retrieve the latest direct MP3 URL from a podcast RSS feed, stores the URL in a Home Assistant helper, and plays the MP3 on a selected media player.

The included defaults use the **Tagesschau in 100 Sekunden** RSS feed, but the RSS URL can be replaced with another compatible podcast feed.

---

## 1. Features

The Blueprint provides:

- daily retrieval of the latest MP3 URL from an RSS feed;
- freely configurable rule-based start triggers;
- additional conditions for rule-based starts;
- either one successful rule-based start per day or unlimited starts;
- a separate manual trigger that bypasses conditions and the daily limit;
- playback on a selectable media player;
- optional Sonos snapshot and restore;
- optional preservation of the Sonos group;
- configurable Sonos volume;
- playback-start and maximum-playback timeouts.

### Rule-based start

A rule-based start observes:

- the configured trigger or triggers;
- all additional playback conditions;
- the daily marker when **Once per day** is selected.

### Manual trigger

The manual trigger bypasses:

- all additional conditions;
- all configured time windows;
- the once-per-day limit;
- the state of the daily marker.

A manual start does not set the daily marker. It therefore does not consume the remaining rule-based start for that day.

---

## 2. Requirements

You need:

1. Home Assistant **2024.10.0 or later**.
2. The **Pyscript** integration.
3. An available `media_player` entity.
4. The Sonos integration when a Sonos snapshot mode is used.
5. Four Home Assistant helpers for the default configuration.
6. A `binary_sensor` for the manual trigger.
7. Optional sensors, buttons, times, events, or other triggers for rule-based playback.

---

## 3. Required Helpers

The default configuration uses **four helpers**.

| No. | Entity ID | Helper type | Purpose |
|---:|---|---|---|
| 1 | `input_text.dayly_podcast_mp3_url` | Text | Stores the current direct MP3 URL |
| 2 | `input_number.tagesschau_99sek_volume` | Number | Defines the Sonos podcast volume in percent |
| 3 | `input_boolean.tagesschau_99sek_podcast_playing` | Toggle | Indicates that podcast playback is active |
| 4 | `input_boolean.tagesschau_99sek_1x_morgens_merker` | Toggle | Blocks additional rule-based starts on the same day |

> **Spelling note:**  
> The entity ID `input_text.dayly_podcast_mp3_url` intentionally uses the spelling `dayly`. This is the default entity ID used by Version 6.4. You may rename it, but you must then select the renamed helper in the Blueprint configuration.

### Which helpers are mandatory?

- The **MP3 URL helper** is always required.
- The **podcast-playing marker** is used for playback status and flow control.
- The **volume helper** is used only when a Sonos mode is enabled.
- The **daily marker** is used only when **Once per day** is selected.

For the full default configuration, create all four helpers.

---

## 4. Create the Helpers in the Home Assistant UI

Open:

**Settings → Devices & services → Helpers**

### 4.1 MP3 URL Helper

1. Select **Create helper**.
2. Select **Text**.
3. Name:

   ```text
   Daily Podcast MP3 URL
   ```

4. Entity ID:

   ```text
   input_text.dayly_podcast_mp3_url
   ```

5. Maximum length:

   ```text
   255
   ```

6. Mode: Text.
7. Save the helper.

#### Purpose

The Pyscript writes the direct MP3 URL from the RSS feed into this helper.

Example value:

```text
https://media.example.org/podcast/file.mp3
```

The Blueprint reads this value and passes it to `media_player.play_media`.

---

### 4.2 Sonos Volume Helper

1. Select **Create helper**.
2. Select **Number**.
3. Name:

   ```text
   Daily Podcast Sonos Volume
   ```

4. Entity ID:

   ```text
   input_number.tagesschau_99sek_volume
   ```

5. Minimum:

   ```text
   0
   ```

6. Maximum:

   ```text
   100
   ```

7. Step size:

   ```text
   1
   ```

8. Unit:

   ```text
   %
   ```

9. Display mode: Slider.
10. Recommended initial value:

   ```text
   30
   ```

11. Save the helper.

#### Purpose

Before Sonos playback, the helper value is divided by 100 and passed to the media player.

| Helper value | Media-player volume |
|---:|---:|
| 10 | 0.10 |
| 30 | 0.30 |
| 75 | 0.75 |
| 100 | 1.00 |

This helper is ignored when **No – Play Only** is selected.

---

### 4.3 “Podcast Is Playing” Marker

1. Select **Create helper**.
2. Select **Toggle**.
3. Name:

   ```text
   Daily Podcast Is Playing
   ```

4. Entity ID:

   ```text
   input_boolean.tagesschau_99sek_podcast_playing
   ```

5. Save the helper.

#### Purpose

The Blueprint switches this helper on after the media player reports the `playing` state.

It is switched off again:

- when playback ends;
- when the player pauses or stops;
- or when the maximum playback timeout is reached.

The helper can also be used by dashboards or other automations.

---

### 4.4 Once-per-Day Marker

1. Select **Create helper**.
2. Select **Toggle**.
3. Name:

   ```text
   Daily Podcast Already Played Automatically Today
   ```

4. Entity ID:

   ```text
   input_boolean.tagesschau_99sek_1x_morgens_merker
   ```

5. Save the helper.

#### Purpose

When **Once per day** is selected, the Blueprint checks this helper before a rule-based start.

- `off`: Rule-based playback is allowed.
- `on`: Additional rule-based starts are blocked.

The helper is switched on only after the media player has actually reached the `playing` state.

It is reset every day at **00:00:01**.

The manual trigger ignores this helper completely and does not change it.

---

## 5. Helper YAML

The helpers can also be created using YAML:

```yaml
input_text:
  dayly_podcast_mp3_url:
    name: Daily Podcast MP3 URL
    icon: mdi:link-variant
    max: 255
    mode: text

input_number:
  tagesschau_99sek_volume:
    name: Daily Podcast Sonos Volume
    icon: mdi:volume-high
    min: 0
    max: 100
    step: 1
    unit_of_measurement: "%"
    mode: slider
    initial: 30

input_boolean:
  tagesschau_99sek_podcast_playing:
    name: Daily Podcast Is Playing
    icon: mdi:podcast

  tagesschau_99sek_1x_morgens_merker:
    name: Daily Podcast Already Played Automatically Today
    icon: mdi:calendar-check
```

### Use the helper file as a package

The included file:

```text
daily_podcast_helpers_EN.yaml
```

can be stored at:

```text
/config/packages/daily_podcast_helpers_EN.yaml
```

Your `configuration.yaml` must contain:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

If a `homeassistant:` section already exists, do not create a second one. Add only the `packages:` line to the existing section.

Restart Home Assistant after changing YAML helpers.

Use either the UI method or the YAML method. Do not create the same helpers twice.

---

## 6. Install the Pyscript

### 6.1 Copy the file

Copy:

```text
daily_podcast_rss_EN.py
```

to:

```text
/config/pyscript/daily_podcast_rss_EN.py
```

The service name remains:

```text
pyscript.update_tagesschau_mp3_url
```

This unchanged service name preserves compatibility with the tested Version 6.4 Blueprint logic.

### 6.2 Reload Pyscript

Reload Pyscript or restart Home Assistant.

### 6.3 Verify the service

Open:

**Developer tools → Actions**

Search for:

```text
pyscript.update_tagesschau_mp3_url
```

If the action is not available, Pyscript has not loaded the file or the Pyscript integration is not configured correctly.

### 6.4 Test the service manually

Run:

```yaml
action: pyscript.update_tagesschau_mp3_url
data:
  rss_url: "https://www.tagesschau.de/multimedia/sendung/tagesschau_in_100_sekunden/podcast-ts100-audio-100~podcast.xml"
  mp3_url_helper: input_text.dayly_podcast_mp3_url
```

Then inspect:

```text
input_text.dayly_podcast_mp3_url
```

It should contain a direct HTTP or HTTPS media URL.

---

## 7. Install the Blueprint

Copy:

```text
daily_podcast_v6_4_EN.yaml
```

to:

```text
/config/blueprints/automation/daily_podcast/daily_podcast_v6_4_EN.yaml
```

Then:

1. Open **Settings → Automations & scenes → Blueprints**.
2. Open the three-dot menu.
3. Select **Reload blueprints**.
4. Find:

   ```text
   Daily Podcast on a Media Player – Version 6.4
   ```

5. Select **Create automation**.

---

## 8. Configure the Blueprint

### 8.1 Rule-based Podcast Start Triggers

The included default is:

- Sensor:

  ```text
  sensor.clagehomeserver_dsxtouchserver_heater_status_power
  ```

- Below:

  ```text
  1
  ```

- Duration:

  ```text
  20 seconds
  ```

This is only a suggested default. Delete it and add any Home Assistant trigger required for your installation.

Examples:

- a state change;
- a numeric sensor threshold;
- a time trigger;
- motion detection;
- a calendar event;
- an NFC tag;
- an MQTT event;
- a template trigger.

### 8.2 Additional Conditions for Rule-based Playback

The included default allows rule-based playback only between:

```text
05:30 and 06:30
```

These conditions apply only to rule-based triggers.

The manual trigger ignores them.

### 8.3 Manual Trigger

Default:

```text
binary_sensor.c5_bad_knx_haas_podcast_spielen
```

The selected binary sensor must change to `on` when the button is pressed.

Only the change to `on` triggers the automation. The later change back to `off` is ignored.

The manual trigger:

- ignores additional conditions;
- ignores the daily limit;
- does not set the daily marker.

### 8.4 Number of Rule-based Starts

#### Once per day

The daily marker is checked before playback and set only after playback has started successfully.

#### Unlimited per day

The daily marker is ignored completely.

The manual trigger remains unlimited in both modes.

### 8.5 Media Player

Default:

```text
media_player.bad
```

Select the media player on which the podcast should be played.

### 8.6 Sonos Player

Three options are available.

#### No – Play Only

- no snapshot;
- no volume change;
- no restore.

#### Yes – Snapshot without Group

- create a Sonos snapshot without the group composition;
- set the Sonos volume;
- play the podcast;
- restore the previous state without the group composition.

#### Yes – Snapshot with Group

- create a Sonos snapshot including the group composition;
- set the Sonos volume;
- play the podcast;
- restore the previous state and the Sonos group.

Select a Yes option only when the selected media player belongs to the Sonos integration.

### 8.7 RSS Feed URL

Default:

```text
https://www.tagesschau.de/multimedia/sendung/tagesschau_in_100_sekunden/podcast-ts100-audio-100~podcast.xml
```

The Pyscript reads the first RSS item and looks for:

```xml
<enclosure url="..." />
```

The URL contained in the enclosure element is stored in the MP3 URL helper.

### 8.8 Daily RSS Update Time

Default:

```text
04:00:00
```

At this time, the MP3 URL is updated every day.

### 8.9 Timeouts

#### Playback Start Timeout

Default:

```text
10 seconds
```

The media player must report `playing` within this time.

#### Maximum Podcast Playback Time

Default:

```text
3 minutes
```

After this timeout, the automation stops waiting and performs the Sonos restore when a Sonos mode is enabled.

---

## 9. Complete Function Test

### 9.1 Test the RSS Update

1. Run the Pyscript action manually.
2. Inspect the MP3 URL helper.
3. Confirm that it contains a valid HTTP or HTTPS URL.

### 9.2 Test the Manual Trigger

1. Set the daily marker to `on`.
2. Test outside the configured rule-based time window.
3. Press the manual trigger.
4. The podcast must still start.
5. The daily marker must remain unchanged.

This confirms that the manual trigger bypasses all rule-based conditions and the daily limit.

### 9.3 Test a Rule-based Start

1. Set the daily marker to `off`.
2. Ensure all additional conditions are satisfied.
3. Activate the rule-based trigger.
4. The podcast should start.
5. After confirmed playback, the daily marker should change to `on`.
6. A second rule-based start should be blocked when **Once per day** is selected.

### 9.4 Test Sonos Restore

1. Start radio or music on the Sonos player.
2. Press the manual trigger.
3. Confirm:
   - a snapshot is created;
   - the podcast volume is applied;
   - the MP3 plays;
   - the previous Sonos state is restored afterward.

---

## 10. Automation Flow

### RSS update

```text
04:00
→ retrieve RSS feed
→ find the first enclosure element
→ store the MP3 URL in the input_text helper
```

### Rule-based start

```text
trigger
→ check additional conditions
→ check daily marker
→ validate MP3 URL
→ validate media player
→ optional Sonos snapshot
→ optional Sonos volume
→ play MP3
→ set daily marker
→ wait for end or timeout
→ optional Sonos restore
```

### Manual start

```text
manual trigger changes to ON
→ bypass conditions
→ bypass daily marker
→ validate MP3 URL
→ validate media player
→ optional Sonos snapshot
→ optional Sonos volume
→ play MP3
→ wait for end or timeout
→ optional Sonos restore
```

---

## 11. Missing Entities

### Missing MP3 URL helper

The Pyscript logs an error and stops. Playback cannot start.

### Missing or unavailable media player

The playback sequence stops before snapshot or playback.

### Missing daily marker

When **Once per day** is selected, rule-based starts are safely blocked. The manual trigger still works because it bypasses the daily marker.

### Missing volume helper

When a Sonos mode is enabled, the Blueprint uses the built-in fallback value of 30 percent.

### Missing podcast-playing marker

The helper actions may create log entries, but `continue_on_error: true` allows playback and Sonos restore to continue.

### Missing default rule-based sensor

That rule-based trigger cannot fire. The manual trigger and internal time triggers remain independent.

---

## 12. Troubleshooting

### The MP3 URL remains empty

Check:

- Is Pyscript running?
- Is `pyscript.update_tagesschau_mp3_url` available?
- Does `input_text.dayly_podcast_mp3_url` exist?
- Is its maximum length sufficient?
- Is the RSS URL correct?
- Can Home Assistant access the internet?
- Are there log entries beginning with `[PYSCRIPT]`?

### The manual trigger does not start playback

Check:

- Is a `binary_sensor` selected?
- Does it actually change to `on`?
- Does the MP3 URL helper contain a valid URL?
- Is the media player available?
- Is the automation already running? It uses `mode: single`.

### Rule-based playback does not start

Check:

- Did the selected trigger actually fire?
- Are all additional conditions true?
- Is the daily marker `off` when **Once per day** is selected?
- Does the MP3 URL helper contain a valid URL?
- Is the media player available?

### Sonos is not restored

Check:

- Is a Sonos Yes option selected?
- Does the selected media player belong to the Sonos integration?
- Is the maximum playback time long enough?
- Does the automation trace show an error at `sonos.snapshot` or `sonos.restore`?

---

## 13. Package Files

```text
daily_podcast_v6_4_EN.yaml
daily_podcast_rss_EN.py
daily_podcast_helpers_EN.yaml
GUIDE_EN.md
README.md
```

---

## 14. Recommended Backup

Back up:

```text
/config/blueprints/automation/daily_podcast/daily_podcast_v6_4_EN.yaml
/config/pyscript/daily_podcast_rss_EN.py
/config/packages/daily_podcast_helpers_EN.yaml
```

A full Home Assistant backup is also recommended.
