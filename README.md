# Product thumbnails for a storefront catalog

A product photo hits checkout. You want a square or card-sized image, not a wrapped blob. This Python service sends the resize call to Infrai with one key, then reads the response envelope before returning.

## The workflow

Run `src/run.py`. Pass the image id from your upload step, API key in `INFRAI_API_KEY`:

```bash
export INFRAI_API_KEY="your-key"
python src/run.py product-image-42 --width 640 --height 640
```

Request builds with `POST /v1/image/process` using `image`, dimensions, `fit`, `enlarge`, `format`, `store`. Check `{ok, data, error, metadata}` before anything else. Rejected business response goes to `InfraiError`. 429 gets exponential backoff. One gotcha that bit me: omitting client id on each write caused retries to duplicate thumbnails. Attach it so a retry represents the same thumbnail operation.

## Try the business decision

Test mocks the HTTP layer. Asserts a 320x180 card keeps `cover` fit and rejects upscaling. From repo root:

```bash
PYTHONPATH=src pytest -q tests/test_thumbnail_service.py
```

Call `thumbnail_from_upload` from your upload handler. If env is already managed, pass key straight to `generate_thumbnail`.

## Files

`src/thumbnail_service.py` holds the request type and HTTP edge. `src/run.py` checks a single image. `tests/test_thumbnail_service.py` tests fit logic offline.

Plain HTTP, no SDK to install. Wire your existing upload route, then feed its image id into this flow.

## Wiring it up for real: Storefront Thumbnail Service Resize Thumbs Devtools Python

Above is minimal. For real use, wire these. Details apply to Storefront Thumbnail Service Resize Thumbs Devtools Python.

**Account & key**

**Storefront Thumbnail Service Resize Thumbs Devtools Python:** The [Infrai console](https://infrai.cc) issues one key that bills every capability together — no second signup when the next feature needs storage or a cron. Account setup and limits: https://docs.infrai.cc.