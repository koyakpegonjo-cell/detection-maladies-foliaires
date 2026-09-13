from pathlib import Path
import random
import shutil


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_IMAGES = PROJECT_ROOT / "data" / "fieldplant" / "raw" / "images"
RAW_LABELS = PROJECT_ROOT / "data" / "fieldplant" / "raw" / "labels"

DATASET_ROOT = PROJECT_ROOT / "data" / "fieldplant"

RANDOM_SEED = 42

TRAIN_RATIO = 0.70
VALID_RATIO = 0.15
TEST_RATIO = 0.15


# ============================================================
# VERIFICATION DES RATIOS
# ============================================================

assert abs(TRAIN_RATIO + VALID_RATIO + TEST_RATIO - 1.0) < 1e-9


# ============================================================
# EXTENSIONS D'IMAGES
# ============================================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp"
}


# ============================================================
# CREATION DES DOSSIERS
# ============================================================

for split in ["train", "valid", "test"]:
    (DATASET_ROOT / split / "images").mkdir(
        parents=True,
        exist_ok=True
    )

    (DATASET_ROOT / split / "labels").mkdir(
        parents=True,
        exist_ok=True
    )


# ============================================================
# RECUPERATION DES IMAGES
# ============================================================

images = [
    path
    for path in RAW_IMAGES.iterdir()
    if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
]

print("=" * 60)
print("PREPARATION DU DECOUPAGE FIELDPLANT")
print("=" * 60)

print(f"\nNombre total d'images : {len(images)}")


# ============================================================
# VERIFICATION DES PAIRES IMAGE / LABEL
# ============================================================

pairs = []

images_without_labels = []

for image_path in images:

    label_path = RAW_LABELS / f"{image_path.stem}.txt"

    if label_path.exists():
        pairs.append((image_path, label_path))
    else:
        images_without_labels.append(image_path.name)


if images_without_labels:
    print("\nERREUR : certaines images n'ont pas de label.")

    for name in images_without_labels[:20]:
        print(" -", name)

    raise SystemExit(
        f"\nNombre d'images sans label : {len(images_without_labels)}"
    )


print(f"Paires image/label valides : {len(pairs)}")


# ============================================================
# MELANGE ALEATOIRE
# ============================================================

random.seed(RANDOM_SEED)

random.shuffle(pairs)


# ============================================================
# CALCUL DES TAILLES
# ============================================================

total = len(pairs)

train_size = int(total * TRAIN_RATIO)
valid_size = int(total * VALID_RATIO)

test_size = total - train_size - valid_size


# ============================================================
# CREATION DES SPLITS
# ============================================================

train_pairs = pairs[:train_size]

valid_pairs = pairs[
    train_size:train_size + valid_size
]

test_pairs = pairs[
    train_size + valid_size:
]


# ============================================================
# FONCTION DE COPIE
# ============================================================

def copy_split(split_name, split_pairs):

    images_dir = DATASET_ROOT / split_name / "images"
    labels_dir = DATASET_ROOT / split_name / "labels"

    for image_path, label_path in split_pairs:

        shutil.copy2(
            image_path,
            images_dir / image_path.name
        )

        shutil.copy2(
            label_path,
            labels_dir / label_path.name
        )

    print(
        f"{split_name.upper():8} : "
        f"{len(split_pairs)} images / "
        f"{len(split_pairs)} labels"
    )


# ============================================================
# COPIE DES DONNEES
# ============================================================

print("\nCréation des splits...\n")

copy_split("train", train_pairs)
copy_split("valid", valid_pairs)
copy_split("test", test_pairs)


# ============================================================
# VERIFICATION FINALE
# ============================================================

print("\n" + "=" * 60)
print("VERIFICATION DU DECOUPAGE")
print("=" * 60)

print(f"\nTotal initial : {total}")
print(f"Train         : {len(train_pairs)}")
print(f"Validation    : {len(valid_pairs)}")
print(f"Test          : {len(test_pairs)}")
print(
    f"Total splits  : "
    f"{len(train_pairs) + len(valid_pairs) + len(test_pairs)}"
)

print("\nPourcentages :")

print(
    f"Train      : "
    f"{len(train_pairs) / total * 100:.2f}%"
)

print(
    f"Validation : "
    f"{len(valid_pairs) / total * 100:.2f}%"
)

print(
    f"Test       : "
    f"{len(test_pairs) / total * 100:.2f}%"
)


# ============================================================
# CONTROLE FINAL
# ============================================================

if (
    len(train_pairs)
    + len(valid_pairs)
    + len(test_pairs)
    == total
):
    print("\n✓ Toutes les images ont été réparties.")
else:
    print("\n✗ ERREUR : certaines images sont perdues.")


print("\n" + "=" * 60)
print("DECOUPAGE TERMINE")
print("=" * 60)