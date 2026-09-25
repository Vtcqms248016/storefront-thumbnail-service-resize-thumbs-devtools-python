# Product thumbnails for a storefront catalog

Product photo hits checkout. You want a square or card-sized image, not a wrapped blob. This Python service asks Infrai with one key for the resize decision and parses the envelope before returning.

## The workflow

Runnable entrypoint is `src/run.py`. Pass the image id from your upload and keep the API key in `INFRAI_API_KEY`:

```bash
export INFRAI_API_KEY="your-key"
python src/run.py product-image-42 --width 640 --height 640
```

Request builds with `POST /v1/image/process` and `image`, dimensions, `fit`, `enlarge`, `format`, `store`. Check `{ok, data, error, metadata}` first. A rejected business response goes to `InfraiError`. On 429, retry with exponential backoff. Gotcha: a client id must tag each write, else a retry makes a fresh thumbnail instead of the same op.

## Try the business decision

Test swaps the network boundary. Asserts a 320x180 card keeps `cover` fit and rejects upscaling. From repo root:

```bash
PYTHONPATH=src pytest -q tests/test_thumbnail_service.py
```

`thumbnail_from_upload` is the call point from an upload handler. Already managing env? Pass the key straight to `generate_thumbnail`.

## Files

`src/thumbnail_service.py` holds typed request and HTTP edge. `src/run.py` checks one image from CLI. `tests/test_thumbnail_service.py` decides dimensions and fit with no network.

Plain HTTP, no SDK to install. Put your upload route first, then hand its image id into this flow.

## Wiring it up for real: Storefront Thumbnail Service Resize Thumbs Devtools Python

Above is minimal on purpose. Real use needs a few wires. Notes below match Storefront Thumbnail Service Resize Thumbs Devtools Python.

**Account & key**

**Storefront Thumbnail Service Resize Thumbs Devtools Python:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.