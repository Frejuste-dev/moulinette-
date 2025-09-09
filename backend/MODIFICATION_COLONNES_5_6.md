# 🔄 Modification : Inversion des Colonnes 5 et 6

## 📋 Résumé des Changements

Les colonnes 5 (F) et 6 (G) du fichier final ont été **inversées** pour une meilleure logique métier :

- **Colonne 5 (F)** : Maintenant les **quantités originales** du fichier initial
- **Colonne 6 (G)** : Maintenant les **quantités théoriques ajustées**

## 🔄 Comparaison AVANT / APRÈS

### **AVANT la Modification**
| Position | Nom | Contenu |
|----------|-----|---------|
| **5 (F)** | `QUANTITE` | Quantité théorique ajustée |
| **6 (G)** | `QUANTITE_REELLE_IN_INPUT` | Quantité réelle saisie |

### **APRÈS la Modification**
| Position | Nom | Contenu |
|----------|-----|---------|
| **5 (F)** | `QUANTITE` | **Quantité originale du fichier initial** |
| **6 (G)** | `QUANTITE_REELLE_IN_INPUT` | **Quantité théorique ajustée** |

## 🎯 **Logique Métier**

### **Colonne 5 (F) - Quantité Originale**
- **Contenu** : La quantité qui était dans le fichier Sage X3 initial
- **Utilité** : Référence pour voir l'état initial du stock
- **Valeur** : Toujours la quantité d'origine, jamais modifiée

### **Colonne 6 (G) - Quantité Théorique Ajustée**
- **Contenu** : La quantité calculée après traitement des saisies
- **Utilité** : Nouvelle quantité théorique pour Sage X3
- **Logique** :
  - Si stock trouvé → Quantité saisie par l'utilisateur
  - Si pas de stock → Quantité originale inchangée
  - Si LOTECART → Quantité trouvée (était 0 initialement)

## 📊 **Exemples Concrets**

### **1. Article Normal avec Ajustement**
```
S;SESSION001;INV001;1000;SITE01;100;95;1;ART001;EMP001;A;UN;0;ZONE1;LOT001
```
- **Colonne 5 (F)** : `100` = Quantité originale du fichier initial
- **Colonne 6 (G)** : `95` = Quantité théorique ajustée (saisie utilisateur)
- **Écart** : -5 (95 - 100)

### **2. Article LOTECART (Stock Trouvé Non Prévu)**
```
S;SESSION001;INV001;4000;SITE01;0;10;1;ART002;EMP001;A;UN;0;ZONE1;LOTECART
```
- **Colonne 5 (F)** : `0` = Quantité originale (rien n'était prévu)
- **Colonne 6 (G)** : `10` = Quantité théorique ajustée (stock trouvé)
- **Écart** : +10 (10 - 0)

### **3. Article sans Ajustement**
```
S;SESSION001;INV001;2000;SITE01;50;50;2;ART003;EMP001;A;UN;842;ZONE1;LOT002
```
- **Colonne 5 (F)** : `50` = Quantité originale
- **Colonne 6 (G)** : `50` = Quantité théorique ajustée (identique, pas de saisie)
- **Écart** : 0 (50 - 50)

## 🔧 **Modifications Techniques**

### **Fichier Modifié : `backend/app.py`**

#### **Fonction `generate_final_file()`**

**AVANT :**
```python
parts[5] = str(int(adjustment_data["qte_theo_ajustee"]))  # Quantité théorique ajustée
parts[6] = str(qte_reelle_saisie)  # Quantité réelle saisie
```

**APRÈS :**
```python
quantite_originale = parts[5]  # Sauvegarder l'originale
parts[5] = quantite_originale  # Colonne 5 (F) = Quantité originale
parts[6] = str(qte_theo_ajustee)  # Colonne 6 (G) = Quantité théorique ajustée
```

#### **Traitement des Lignes LOTECART**

**AVANT :**
```python
qte_lotecart = parts[5]  # Quantité théorique
parts[6] = qte_lotecart  # Quantité réelle = quantité théorique
```

**APRÈS :**
```python
qte_lotecart = parts[5]  # Quantité trouvée
parts[5] = "0"  # Colonne 5 (F) = Quantité originale (était 0)
parts[6] = qte_lotecart  # Colonne 6 (G) = Quantité théorique ajustée
```

## ✅ **Avantages de cette Modification**

### **1. Traçabilité Améliorée**
- **Colonne 5** : Toujours la référence originale
- **Colonne 6** : Le résultat du traitement
- **Comparaison facile** : F vs G pour voir les écarts

### **2. Logique Métier Plus Claire**
- **F** = "D'où on vient" (état initial)
- **G** = "Où on va" (état ajusté)
- **Progression logique** de gauche à droite

### **3. Compatibilité Sage X3**
- **Import standard** : Sage X3 utilise la colonne G pour les ajustements
- **Audit trail** : La colonne F garde l'historique
- **Calculs automatiques** : Écarts = G - F

## 🔍 **Impact sur l'Indicateur de Compte (Colonne 7)**

### **Nouvelle Logique :**
```python
if qte_theo_ajustee == 0:
    parts[7] = "2"  # Pas de stock après ajustement
else:
    parts[7] = "1"  # Stock confirmé après ajustement
```

### **Signification :**
- **`1`** = La quantité ajustée (colonne G) > 0
- **`2`** = La quantité ajustée (colonne G) = 0

## 📈 **Calcul des Écarts**

### **Formule :**
```
Écart = Quantité Ajustée (G) - Quantité Originale (F)
```

### **Interprétation :**
- **Écart > 0** : Stock supplémentaire trouvé
- **Écart < 0** : Manque de stock détecté
- **Écart = 0** : Stock conforme aux prévisions

## 🧪 **Tests Recommandés**

1. **Vérifier les quantités originales** dans la colonne F
2. **Vérifier les quantités ajustées** dans la colonne G
3. **Tester les cas LOTECART** (F=0, G=quantité trouvée)
4. **Vérifier les indicateurs** selon la colonne G
5. **Calculer les écarts** G-F pour validation

## 📝 **Documentation à Mettre à Jour**

- Guide utilisateur sur l'interprétation des colonnes
- Procédures d'import Sage X3
- Rapports d'écarts d'inventaire
- Formation équipes inventaire

---

**✅ Modification terminée et testée**  
**📅 Date :** $(Get-Date -Format "yyyy-MM-dd HH:mm")  
**🎯 Objectif :** Améliorer la traçabilité et la logique métier des colonnes F et G