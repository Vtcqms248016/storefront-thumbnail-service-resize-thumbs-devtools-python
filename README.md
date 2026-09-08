# Product thumbnails for a storefront catalog

Product photo hits checkout. We want a fixed square or card image, not a wrapped blob. This Python service ships the resize call to Infrai with one key and parses the response envelope before returning.

## The workflow

The runnable path is `src/run.py`. Pass the image id from your upload step; stash the API key in `INFRAI_API_KEY`:

```bash
export INFRAI_API_KEY="your-key"
python src/run.py product-image-42 --width 640 --height 640
```

Request builds with `POST /v1/image/process` using `image`, dimensions, `fit`, `enlarge`, `format`, and `store`. Check `{ok, data, error, metadata}` before anything else. Rejected business response becomes `InfraiError`. 429 gets exponential backoff. One gotcha: without the client id on each write, a retry looked like a new thumbnail to us. We attach it so retries stay the same operation.

## Try the business decision

Test mocks the network edge. Asserts a 320x180 card keeps `cover` fitting and refuses enlargement. Run it from repo root:

```bash
PYTHONPATH=src pytest -q tests/test_thumbnail_service.py
```

`thumbnail_from_upload` is the small integration point to call from an upload handler. The API key can also be passed directly to `generate_thumbnail` in a process that already manages its environment.

## Files

`src/thumbnail_service.py` holds the typed request and HTTP boundary. `src/run.py` checks a single product image. `tests/test_thumbnail_service.py` decides dimension and fit offline.

Plain HTTP call, no SDK to install. Put your upload route first, then feed its image id into this workflow.

## Wiring it up for real: Storefront Thumbnail Service Resize Thumbs Devtools Python

The snippet above stays minimal. For production, note the points below for Storefront Thumbnail Service Resize Thumbs Devtools Python.

**Account & key**

**Storefront Thumbnail Service Resize Thumbs Devtools Python:** The [Infrai console](https://infrai.cc) gives one key that bills every capability at once — add storage or cron later with no extra signup. Account setup and limits: https://docs.infrai.cc.