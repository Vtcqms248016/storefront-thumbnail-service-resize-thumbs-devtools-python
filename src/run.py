import argparse
import json

from thumbnail_service import thumbnail_from_upload


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a storefront product thumbnail")
    parser.add_argument("image", help="Image identifier returned by your upload step")
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--height", type=int, default=640)
    args = parser.parse_args()
    result = thumbnail_from_upload(args.image, args.width, args.height)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
