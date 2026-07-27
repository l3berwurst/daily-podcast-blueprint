# Daily Podcast on a Media Player – Version 6.4

A Home Assistant automation Blueprint that retrieves the latest MP3 from a podcast RSS feed and plays it on a selected media player.

The package is optimized for Sonos. It can also be used with other media players by selecting **No – Play Only**.

## Features

- daily RSS feed update;
- automatic extraction of the direct MP3 URL;
- freely configurable rule-based triggers;
- additional conditions for rule-based starts;
- once-per-day or unlimited rule-based playback;
- separate manual trigger that bypasses conditions and the daily limit;
- Sonos snapshot and restore;
- optional Sonos group preservation;
- configurable Sonos volume;
- playback-start and maximum-playback timeouts.

## Included Files

| File | Purpose |
|---|---|
| `daily_podcast_v6_4_EN.yaml` | English automation Blueprint |
| `daily_podcast_rss_EN.py` | English Pyscript with compatible service name |
| `daily_podcast_helpers_EN.yaml` | YAML package containing the required helpers |
| `GUIDE_EN.md` | Full English step-by-step guide |
| `README.md` | Quick overview and installation |

## Requirements

- Home Assistant 2024.10.0 or later;
- Pyscript;
- an existing media player;
- the Sonos integration when snapshot mode is used;
- the four helpers listed below;
- a `binary_sensor` for the manual trigger.

## Required Helpers

The default configuration uses **four helpers**.

| Entity ID | Type | Purpose |
|---|---|---|
| `input_text.dayly_podcast_mp3_url` | Text | Stores the direct MP3 URL |
| `input_number.tagesschau_99sek_volume` | Number | Sonos volume from 0 to 100 percent |
| `input_boolean.tagesschau_99sek_podcast_playing` | Toggle | Indicates active podcast playback |
| `input_boolean.tagesschau_99sek_1x_morgens_merker` | Toggle | Blocks additional rule-based starts on the same day |

### Helper YAML

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

The included `daily_podcast_helpers_EN.yaml` file contains the same configuration as a Home Assistant package.

## Quick Installation

### 1. Create the helpers

Use:

```text
Settings → Devices & services → Helpers
```

or install `daily_podcast_helpers_EN.yaml` as a package.

### 2. Copy the Pyscript

```text
daily_podcast_rss_EN.py
→ /config/pyscript/daily_podcast_rss_EN.py
```

Reload Pyscript or restart Home Assistant.

The service remains:

```text
pyscript.update_tagesschau_mp3_url
```

### 3. Copy the Blueprint

```text
daily_podcast_v6_4_EN.yaml
→ /config/blueprints/automation/daily_podcast/daily_podcast_v6_4_EN.yaml
```

Reload the Blueprints.

### 4. Create the automation

```text
Settings
→ Automations & scenes
→ Blueprints
→ Daily Podcast on a Media Player – Version 6.4
→ Create automation
```

## Included Defaults

### Rule-based start

```text
sensor.clagehomeserver_dsxtouchserver_heater_status_power
below 1
for 20 seconds
```

### Additional condition

```text
05:30 to 06:30
```

### Manual trigger

```text
binary_sensor.c5_bad_knx_haas_podcast_spielen
```

### RSS feed

```text
https://www.tagesschau.de/multimedia/sendung/tagesschau_in_100_sekunden/podcast-ts100-audio-100~podcast.xml
```

### Daily RSS update

```text
04:00
```

### Sonos

```text
Media player: media_player.bad
Mode: Yes – Snapshot with Group
Volume helper: input_number.tagesschau_99sek_volume
```

## Manual Trigger and Daily Limit

The manual trigger bypasses:

- all additional conditions;
- configured time windows;
- the once-per-day limit;
- the daily marker.

A manual start does not set the daily marker.

Rule-based starts observe all configured conditions. When **Once per day** is selected, the marker is set only after playback has started successfully.

The daily marker is reset at **00:00:01** every day.

## Sonos Modes

### No – Play Only

No snapshot, volume, or restore action is performed.

### Yes – Snapshot without Group

The Sonos state is stored and restored without preserving group composition.

### Yes – Snapshot with Group

The Sonos state and group composition are stored and restored.

## Manual Pyscript Test

```yaml
action: pyscript.update_tagesschau_mp3_url
data:
  rss_url: "https://www.tagesschau.de/multimedia/sendung/tagesschau_in_100_sekunden/podcast-ts100-audio-100~podcast.xml"
  mp3_url_helper: input_text.dayly_podcast_mp3_url
```

After a successful request, `input_text.dayly_podcast_mp3_url` contains a direct MP3 URL.

## Full Documentation

See:

```text
GUIDE_EN.md
```

for complete installation steps, helper descriptions, configuration, tests, automation flow, missing-entity behavior, and troubleshooting.

## Compatibility Note

The internal input keys, entity defaults, trigger IDs, service calls, and automation logic are unchanged from the tested German Version 6.4.

The entity ID `input_text.dayly_podcast_mp3_url` intentionally retains the spelling `dayly` for compatibility.
