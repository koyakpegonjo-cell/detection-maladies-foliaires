from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_ROOT = PROJECT_ROOT / "data" / "fieldplant"


def get_image_stems(split):

    images_dir = DATASET_ROOT / split / "images"

    extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp"
    }

    return {
        image.stem
        for image in images_dir.iterdir()
        if image.is_file()
        and image.suffix.lower() in extensions
    }


train = get_image_stems("train")
valid = get_image_stems("valid")
test = get_image_stems("test")


print("=" * 60)
print("VERIFICATION DES SPLITS FIELDPLANT")
print("=" * 60)

print(f"\nTrain      : {len(train)}")
print(f"Validation : {len(valid)}")
print(f"Test       : {len(test)}")


train_valid = train & valid
train_test = train & test
valid_test = valid & test

all_images = train | valid | test


print("\n" + "=" * 60)
print("VERIFICATION DES CHEVAUCHEMENTS")
print("=" * 60)

print(f"\nTrain ∩ Validation : {len(train_valid)}")
print(f"Train ∩ Test       : {len(train_test)}")
print(f"Validation ∩ Test  : {len(valid_test)}")

print(f"\nImages uniques     : {len(all_images)}")


if not train_valid and not train_test and not valid_test:
    print("\n✓ AUCUN CHEVAUCHEMENT DETECTE")
else:
    print("\n✗ ATTENTION : DES DOUBLONS ONT ETE DETECTES")


if len(all_images) == 5156:
    print("✓ Les 5156 images sont présentes une seule fois.")
else:
    print(
        f"✗ Nombre inattendu d'images uniques : {len(all_images)}"
    )


print("\n" + "=" * 60)