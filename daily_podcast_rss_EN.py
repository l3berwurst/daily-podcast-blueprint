import aiohttp
import xml.etree.ElementTree as ET


@service
async def update_tagesschau_mp3_url(rss_url=None, mp3_url_helper=None):
    """
    Reads the latest MP3 URL from the supplied RSS feed and stores it in the
    supplied input_text helper.

    Expected service data:
      rss_url: URL of the RSS feed
      mp3_url_helper: Entity ID of the input_text helper used for the MP3 URL
    """

    rss_url = str(rss_url or "").strip()
    mp3_url_helper = str(mp3_url_helper or "").strip()

    if not rss_url.startswith(("http://", "https://")):
        log.error(
            f"[PYSCRIPT] Invalid RSS URL supplied: {rss_url!r}"
        )
        return

    if not mp3_url_helper.startswith("input_text."):
        log.error(
            "[PYSCRIPT] Invalid MP3 helper supplied. "
            f"Expected input_text.*, received: {mp3_url_helper!r}"
        )
        return

    if not state.exist(mp3_url_helper):
        log.error(
            "[PYSCRIPT] The selected MP3 helper does not exist: "
            f"{mp3_url_helper}. Create an input_text helper first or select "
            "an existing entity in the Blueprint."
        )
        return

    timeout = aiohttp.ClientTimeout(total=20)
    headers = {"User-Agent": "HomeAssistant-Pyscript/Daily-Podcast-RSS"}

    try:
        async with aiohttp.ClientSession(
            timeout=timeout,
            headers=headers,
        ) as session:
            async with session.get(rss_url) as response:
                if response.status != 200:
                    log.error(
                        "[PYSCRIPT] RSS request failed: "
                        f"HTTP {response.status}, URL: {rss_url}"
                    )
                    return

                content = await response.read()

        root = ET.fromstring(content)
        enclosure = root.find(".//item/enclosure")

        if enclosure is None:
            log.warning(
                "[PYSCRIPT] No enclosure element was found in the first RSS item."
            )
            return

        latest_url = enclosure.attrib.get("url", "").strip()

        if not latest_url.startswith(("http://", "https://")):
            log.warning(
                f"[PYSCRIPT] Invalid or missing MP3 URL: {latest_url!r}"
            )
            return

        previous_url = state.get(mp3_url_helper)

        if previous_url == latest_url:
            log.info(
                f"[PYSCRIPT] The MP3 URL in {mp3_url_helper} is already current."
            )
            return

        state.set(mp3_url_helper, latest_url)
        current_value = state.get(mp3_url_helper)

        log.info(
            "[PYSCRIPT] New MP3 URL stored: "
            f"{mp3_url_helper} = {current_value}"
        )

    except aiohttp.ClientError as err:
        log.error(
            f"[PYSCRIPT] Network error while retrieving RSS feed {rss_url}: {err}"
        )
    except ET.ParseError as err:
        log.error(
            f"[PYSCRIPT] RSS feed could not be parsed as XML: {err}"
        )
    except Exception as err:
        log.error(f"[PYSCRIPT] Unexpected error: {err}")
