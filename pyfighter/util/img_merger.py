"""Script used to merge background into one image 5(256) x 4(256)"""

from PIL import Image

BG_TILE_PATH = "./pyfighter/assets/kenney_space-shooter-redux/Backgrounds/black.png"


def main():
    """Main merger method."""

    tile = Image.open(BG_TILE_PATH)
    bg_img = Image.new("RGB", (256 * 5, 256 * 4))
    x = 0
    y = 0
    for _ in range(4):
        for _ in range(5):
            bg_img.paste(tile, (x, y))
            x += 256
        x = 0
        y += 256

    bg_img.save("./bg_merged.png", format="PNG", subsampling=0, quality=100)


if __name__ == "__main__":
    main()
