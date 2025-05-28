# Securitary-NX

Securitary-NX est une application de bureau moderne et sécurisée pour générer des mots de passe robustes et personnalisés. Elle offre une interface graphique intuitive, un mode sombre/clair, la génération massive de mots de passe, l'export, la copie rapide, et un haut niveau de sécurité grâce à l'utilisation de sources aléatoires cryptographiquement sûres.

## Fonctionnalités principales
- Génération de mots de passe sécurisés et personnalisables (longueur jusqu'à 1 000 000 caractères)
- Choix des types de caractères (majuscules, minuscules, chiffres, symboles, exclusion des ambigus)
- Génération multiple (plusieurs mots de passe en une fois)
- Export TXT/CSV
- Copie rapide (individuelle ou en lot)
- Interface moderne avec thème sombre/clair
- Barre de menu (Fichier, Aide)
- Modal "À propos" avec informations sur le créateur
- Indicateur de progression et consommation CPU/mémoire lors de la génération massive
- Optimisation multi-cœur (jusqu'à 4 cœurs)

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/YelielGerardK/Securitary-NX.git
   cd Securitary-NX
   ```
2. Créez un environnement virtuel et installez les dépendances :
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate sous Windows
   pip install -r requirements.txt
   ```

## Utilisation

Lancez l'application :
```bash
python main.py
```

## Exemple d'utilisation
- Choisissez la longueur et les options de caractères
- Cliquez sur "Générer" pour obtenir un ou plusieurs mots de passe
- Copiez ou exportez vos mots de passe en un clic

## Contribution
Les contributions sont les bienvenues ! Merci de proposer vos améliorations via des issues ou des pull requests.

## Licence
Ce projet est sous licence MIT.

## À propos
- **Nom du logiciel** : Securitary-NX
- **Créateur** : Rabenandrasana Yeliel Gerard
- **Version** : v1.0.0
- **Description** : Un générateur de mots de passe sécurisé et personnalisable.

## Structure du projet

```
Securitary/
├── assets/
│   ├── logo.png               # Logo de l'application
│   ├── background.png         # Image de fond pour l'interface
├── config/
│   ├── app_config.py          # Configuration globale de l'application
│   ├── settings.json          # Paramètres utilisateur ou par défaut
├── core/
│   ├── password_generator.py  # Logique principale de génération de mot de passe
│   ├── utils.py               # Fonctions utilitaires pour le cœur de l'application
├── gui/
│   ├── main_window.py         # Fenêtre principale de l'application
│   ├── widgets.py             # Widgets personnalisés pour l'interface
├── output/
│   ├── generated_passwords.txt # Fichier temporaire pour les mots de passe exportés
├── resources/
│   ├── icons/
│   │   ├── copy_icon.png      # Icône pour le bouton "Copier"
│   │   ├── generate_icon.png  # Icône pour le bouton "Générer"
├── services/
│   ├── clipboard_service.py   # Service pour interagir avec le presse-papiers
│   ├── file_export_service.py # Service pour exporter les mots de passe
├── ui/
│   ├── styles.qss             # Feuille de style pour l'interface graphique
├── utils/
│   ├── validation.py          # Validation des entrées utilisateur
│   ├── logger.py              # Gestion des logs pour le débogage
├── LICENSE                    # Licence du projet
├── README.md                  # Documentation du projet
├── main.py                    # Point d'entrée de l'application
└── requirements.txt           # Liste des dépendances Python
```


## Auteurs
- Rabenandrasana Yeliel Gerard
