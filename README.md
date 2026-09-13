# Détection de maladies foliaires par YOLO

Projet de vision par ordinateur : fine-tuning d'un modèle **YOLO11n** pour la détection et la classification de maladies foliaires (manioc, maïs, tomate) sur des images de terrain, à des fins d'aide au diagnostic phytosanitaire précoce.

> Réalisé par : **KOYAKPEGON Josué**
> Durée du projet : 10 jours
> Environnement d'entraînement : **CPU uniquement** (Intel Core i7-8650U, sans GPU)

---

## 1. Objectif

Concevoir, entraîner et évaluer un système de détection d'objets basé sur YOLO capable de localiser (bounding box) et classer des maladies foliaires sur des photos de plantes prises en conditions de terrain (champ, serre, jardin).

## 2. Jeu de données

Dataset public **FieldPlant** (Roboflow Universe) : images prises en conditions réelles de champ, annotées en bounding boxes par des experts en pathologie végétale.

- Source : https://universe.roboflow.com/plant-disease-detection/fieldplant
- 27 classes (manioc, maïs, tomate — état sain + maladies)
- Répartition : 3 609 images (train) / 773 (validation) / 774 (test), soit 5 156 images uniques, sans chevauchement entre les splits

## 3. Structure du projet

```
NOM_Prenom_ProjetCV_DetectionMaladiesFoliaires/
├── README.md                     # Ce fichier
├── rapport_maladies_foliaires.docx   # Rapport d'expérimentation complet
├── notebooks/
│   └── finetuning_yolo.ipynb     # Notebook principal (vérification, entraînement, évaluation)
├── configs/
│   └── data.yaml                 # Configuration YOLO (classes, chemins train/val/test)
├── data/
│   └── fieldplant/
│       ├── train/{images,labels}
│       ├── valid/{images,labels}
│       └── test/{images,labels}
└── runs/                         # Généré automatiquement par Ultralytics
    ├── fieldplant_test/          # Entraînement de test (3 époques)
    ├── fieldplant_30epochs/      # Entraînement principal (30 époques)
    │   └── weights/best.pt       # Modèle final fine-tuné
    └── fieldplant_test_evaluation/  # Évaluation finale sur le jeu de test
```

> Le dossier `data/fieldplant` n'est pas versionné dans l'archive rendue (poids et images trop volumineux) : il doit être téléchargé depuis Roboflow Universe et placé à cet emplacement avant de relancer le notebook. Le dossier `runs/` est régénéré automatiquement à chaque exécution de l'entraînement.

## 4. Installation

```bash
pip install ultralytics opencv-python matplotlib pandas pyyaml pillow numpy seaborn scikit-learn
```

Le notebook a été exécuté avec **Python 3.13** et **PyTorch 2.14.0 (build CPU)**.

## 5. Utilisation

1. Placer le dataset FieldPlant dans `data/fieldplant/` (structure train/valid/test déjà annotée au format YOLO).
2. Vérifier que `configs/data.yaml` pointe vers les bons chemins et déclare bien 27 classes.
3. Ouvrir `notebooks/finetuning_yolo.ipynb` et exécuter les cellules dans l'ordre :
   - Vérification et exploration du dataset
   - Test rapide d'entraînement (3 époques) — sert de contrôle avant l'entraînement long
   - Entraînement principal (30 époques)
   - Évaluation finale sur le jeu de test

 **Sans GPU, l'entraînement principal (30 époques) prend environ 34 heures sur un CPU de type i7 portable.** Prévoir de le lancer en arrière-plan sur une période longue (nuit + journée).

## 6. Résultats obtenus

Modèle : **YOLO11n**, 2 587 417 paramètres, 6,4 GFLOPs.

| Métrique | Test rapide (3 ép.) | Entraînement principal (30 ép.) | Évaluation finale (test) |
|---|---|---|---|
| Precision | 0.618 | 0.548 | 0.493 |
| Recall | 0.222 | 0.599 | 0.592 |
| mAP@0.5 | 0.241 | 0.597 | 0.559 |
| mAP@0.5:0.95 | 0.179 | 0.471 | 0.436 |

Temps d'inférence mesuré sur CPU : ~114 ms/image (~8 images/seconde). Détail complet des métriques par classe, courbes d'apprentissage et analyse qualitative des erreurs : voir `rapport_maladies_foliaires.docx`.

## 7. Limites connues

- Fort déséquilibre entre classes (certaines maladies rares comptent moins de 10 exemples d'entraînement).
- Deux libellés de classes dupliqués dans `data.yaml` d'origine (« Charbon du maïs » et « Décoloration violette du maïs »).
- Faute de GPU, aucune comparaison nano/small n'a pu être réalisée dans le délai imparti.

## 8. Modalités de rendu

- Destinataire : amadoualwalyndiaye@gmail.com
- Objet du mail : *Projet CV - Détection de maladies foliaires (YOLO)*
- Archive `.zip` unique contenant le rapport et le code, nommée : `NOM_Prenom_ProjetCV_DetectionMaladiesFoliaires.zip` (nom de famille en majuscules, sans espaces ni accents)