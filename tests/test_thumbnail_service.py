import json

from thumbnail_service import ThumbnailRequest, generate_thumbnail


def test_thumbnail_request_keeps_catalog_dimensions(monkeypatch):
    seen = {}

    def fake_post(payload, key):
        seen.update(payload)
        return {"ok": True, "data": {"image": "thumb-1"}}

    monkeypatch.setattr("thumbnail_service._post_process", fake_post)
    result = generate_thumbnail(ThumbnailRequest("product-42", 320, 180), "test-key")
    assert result["data"]["image"] == "thumb-1"
    assert seen["image"] == "product-42"
    assert (seen["width"], seen["height"], seen["fit"]) == (320, 180, "cover")
    assert seen["enlarge"] is False
