# 📄 Structure du Fichier Final Sage X3

## 🎯 **Vue d'Ensemble**

Le fichier final généré est un **fichier CSV** au format Sage X3 qui contient :
- Les **en-têtes** originaux (lignes E; et L;)
- Les **lignes de données** modifiées (lignes S;) avec les quantités réelles saisies
- Les **nouvelles lignes LOTECART** (si applicable)

## 📋 **Format Général**

```
E;[en-tête session]
L;[en-tête inventaire]
S;[ligne de données 1]
S;[ligne de données 2]
...
S;[nouvelles lignes LOTECART]
```

## 🔍 **Structure Détaillée des Colonnes**

### **Lignes de Données (S;)**

Chaque ligne de données contient **15 colonnes** séparées par des **point-virgules (;)** :

| Position | Nom Colonne | Description | Exemple | Modifications |
|----------|-------------|-------------|---------|---------------|
| **0** | `TYPE_LIGNE` | Type de ligne (toujours "S" pour les données) | `S` | ❌ **Inchangé** |
| **1** | `NUMERO_SESSION` | Identifiant unique de la session d'inventaire | `BKE022508SES00000004` | ❌ **Inchangé** |
| **2** | `NUMERO_INVENTAIRE` | Identifiant de l'inventaire | `BKE022508INV00000008` | ❌ **Inchangé** |
| **3** | `RANG` | Numéro de ligne unique dans le fichier | `1000`, `2000`, `3000` | ❌ **Inchangé** |
| **4** | `SITE` | Code du site/dépôt | `BKE02`, `CPKU` | ❌ **Inchangé** |
| **5** | `QUANTITE` | **Quantité originale du fichier initial** | `100`, `0` | ✅ **MODIFIÉ** |
| **6** | `QUANTITE_REELLE_IN_INPUT` | **Quantité théorique ajustée** | `95`, `10` | ✅ **MODIFIÉ** |
| **7** | `INDICATEUR_COMPTE` | Indicateur de statut du compte | `1`, `2` | ✅ **MODIFIÉ** |
| **8** | `CODE_ARTICLE` | Code de l'article inventorié | `37CV045045GAM` | ❌ **Inchangé** |
| **9** | `EMPLACEMENT` | Emplacement physique de stockage | `BKE02`, `A01` | ❌ **Inchangé** |
| **10** | `STATUT` | Statut de l'article | `AM`, `A` | ❌ **Inchangé** |
| **11** | `UNITE` | Unité de mesure | `UN`, `KG` | ❌ **Inchangé** |
| **12** | `VALEUR` | Valeur monétaire (souvent 0) | `0`, `842` | ❌ **Inchangé** |
| **13** | `ZONE_PK` | Zone de picking/stockage | `BKE2`, `ZONE1` | ❌ **Inchangé** |
| **14** | `NUMERO_LOT` | Numéro de lot original | `LOT311223`, `LOTECART` | ❌ **Inchangé** |

## 🔧 **Colonnes Modifiées par le Processus**

### **Colonne 5 : QUANTITE (Quantité Originale)**
- **Avant** : Quantité théorique originale du système
- **Après** : **Quantité originale du fichier initial (inchangée)**
- **Utilité** : Référence pour calculer les écarts et garder la traçabilité

### **Colonne 6 : QUANTITE_REELLE_IN_INPUT (Quantité Théorique Ajustée)**
- **Avant** : Toujours `0` (pas de saisie)
- **Après** : **Quantité théorique ajustée selon les saisies**
- **Logique** : 
  - Si stock trouvé → Quantité saisie par l'utilisateur
  - Si pas de stock → Quantité originale inchangée
  - Si LOTECART → Quantité trouvée (était 0 initialement)

### **Colonne 7 : INDICATEUR_COMPTE**
- **Avant** : Généralement `1`
- **Après** : 
  - `1` = Quantité réelle > 0 (stock confirmé)
  - `2` = Quantité réelle = 0 (pas de stock trouvé)

## 📊 **Exemples Concrets**

### **Ligne Normale (avec stock trouvé)**
```
S;BKE022508SES00000004;BKE022508INV00000008;1000;BKE02;100;95;1;37CV045045GAM;BKE02;AM;UN;0;BKE2;LOT311223
```

**Décomposition :**
- Article `37CV045045GAM` 
- Quantité originale : `100` (colonne 5) - Référence initiale
- Quantité théorique ajustée : `95` (colonne 6) - Après saisie ✅
- **Écart : -5** (95 - 100)
- Indicateur : `1` (stock confirmé)
- Lot original : `LOT311223`

### **Ligne LOTECART (stock trouvé non prévu)**
```
S;BKE022508SES00000004;BKE022508INV00000008;4000;BKE02;0;10;1;37CV150150GAM;BKE02;AM;UN;0;BKE2;LOTECART
```

**Décomposition :**
- Article `37CV150150GAM`
- Quantité originale : `0` (colonne 5) - Rien n'était prévu
- Quantité théorique ajustée : `10` (colonne 6) - Stock trouvé ✅
- **Écart : +10** (10 - 0)
- Indicateur : `1` (stock trouvé)
- Lot spécial : `LOTECART`

### **Ligne sans Stock (rien trouvé)**
```
S;BKE022508SES00000004;BKE022508INV00000008;2000;BKE02;50;50;2;32BTCS2GAM;BKE02;AM;UN;842;BKE2;LOT240101
```

**Décomposition :**
- Article `32BTCS2GAM`
- Quantité originale : `50` (colonne 5) - Référence initiale
- Quantité théorique ajustée : `50` (colonne 6) - Inchangée (pas de saisie)
- **Écart : 0** (50 - 50)
- Indicateur : `2` (pas de stock trouvé)
- Lot original : `LOT240101`

## 🎯 **Logique de Traitement**

### **1. Lignes Existantes**
```python
# Pour chaque ligne originale
if ajustement_existe:
    parts[5] = quantite_reelle_saisie    # Quantité théorique = réelle
    parts[6] = quantite_reelle_saisie    # Quantité réelle saisie
    parts[7] = "1" if qte_reelle > 0 else "2"  # Indicateur
else:
    parts[6] = "0"    # Pas de saisie = 0
    parts[7] = "2"    # Indicateur = pas de stock
```

### **2. Nouvelles Lignes LOTECART**
```python
# Création automatique pour stock trouvé non prévu
nouveau_rang = max_rang + 1000
parts[3] = str(nouveau_rang)           # Nouveau numéro de ligne
parts[5] = str(quantite_trouvee)       # Quantité théorique = trouvée
parts[6] = str(quantite_trouvee)       # Quantité réelle = trouvée
parts[7] = "1"                         # Indicateur = stock confirmé
parts[14] = "LOTECART"                 # Lot spécial
```

## 📈 **Traçabilité et Audit**

### **Informations Conservées**
- ✅ **Quantités originales** (dans les logs/base de données)
- ✅ **Quantités réelles saisies** (colonne 6)
- ✅ **Numéros de lot originaux** (colonne 14)
- ✅ **Horodatage** des modifications (métadonnées session)

### **Informations Calculées**
- ✅ **Écarts** = Quantité réelle - Quantité théorique originale
- ✅ **Ajustements** appliqués selon stratégie (FIFO/LIFO)
- ✅ **Nouveaux lots LOTECART** créés automatiquement

## 🔍 **Points Clés pour l'Utilisateur**

### **1. Colonne F (Position 5) = QUANTITÉ ORIGINALE**
- **Référence initiale** : Quantité qui était dans le fichier Sage X3 d'origine
- **Traçabilité** : Permet de voir l'état initial du stock
- **Calcul d'écarts** : Base de comparaison avec la colonne G

### **2. Colonne G (Position 6) = QUANTITÉ THÉORIQUE AJUSTÉE**
- **C'est LA colonne** qui contient les quantités après traitement
- **Import Sage X3** : Cette colonne sera utilisée pour les ajustements de stock
- **Logique** : Résultat du traitement des saisies utilisateur

### **3. Indicateurs de Compte (Colonne 7)**
- `1` = **Stock confirmé** (quantité ajustée > 0)
- `2` = **Pas de stock** (quantité ajustée = 0)

### **4. Lots LOTECART**
- **Création automatique** quand du stock est trouvé alors que rien n'était prévu
- **Colonne F** = 0 (quantité originale)
- **Colonne G** = quantité trouvée (quantité ajustée)
- **Numéro de lot** = "LOTECART" (identifiable facilement)
- **Nouvelles lignes** ajoutées à la fin du fichier

### **5. Calcul des Écarts**
- **Formule** : Écart = Colonne G - Colonne F
- **Écart positif** : Stock supplémentaire trouvé
- **Écart négatif** : Manque de stock détecté
- **Écart zéro** : Stock conforme aux prévisions

## 📁 **Nom du Fichier Final**

**Format :** `[nom_original]_corrige_[session_id].csv`

**Exemple :** `BKE_inventaire_240825_corrige_a1b2c3d4.csv`

---

**✅ Le fichier final est prêt pour l'import dans Sage X3**  
**📊 Colonne F = Quantités originales | Colonne G = Quantités ajustées**  
**🔍 Traçabilité complète : F (d'où on vient) → G (où on va)**  
**📈 Calcul d'écarts : G - F = Impact de l'inventaire**