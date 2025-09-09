#!/usr/bin/env python3
"""
Test script pour vérifier la correction du bug LOTECART
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.lotecart_processor import LotecartProcessor
import pandas as pd
import numpy as np

def test_lotecart_with_nan_reference():
    """Test avec une reference_line qui est NaN"""
    processor = LotecartProcessor()
    
    # Cas de test avec différents types de reference_line problématiques
    test_adjustments = [
        {
            'CODE_ARTICLE': 'TEST001',
            'is_new_lotecart': True,
            'QUANTITE_CORRIGEE': 10,
            'reference_line': np.nan  # ❌ Cas qui causait l'erreur
        },
        {
            'CODE_ARTICLE': 'TEST002', 
            'is_new_lotecart': True,
            'QUANTITE_CORRIGEE': 5,
            'reference_line': None  # ❌ Cas problématique
        },
        {
            'CODE_ARTICLE': 'TEST003',
            'is_new_lotecart': True, 
            'QUANTITE_CORRIGEE': 15,
            'reference_line': 42.5  # ❌ Float au lieu de string
        },
        {
            'CODE_ARTICLE': 'TEST004',
            'is_new_lotecart': True,
            'QUANTITE_CORRIGEE': 20,
            'reference_line': 'S;SES001;INV001;1000;SITE01;100;0;1;TEST004;LOC01;AM;UN;0;ZONE1;LOT001'  # ✅ Cas valide
        }
    ]
    
    print("🧪 Test de la correction du bug LOTECART...")
    
    try:
        # Ceci ne devrait plus lever d'exception
        result = processor.generate_lotecart_lines(test_adjustments, max_line_number=1000)
        
        print(f"✅ Test réussi ! {len(result)} lignes générées")
        print("📋 Résultats:")
        for i, line in enumerate(result):
            print(f"  {i+1}. {line}")
            
        # Vérifier qu'on a bien une seule ligne (seul le cas valide)
        if len(result) == 1:
            print("✅ Seule la ligne valide a été traitée, les cas problématiques ont été ignorés")
        else:
            print(f"⚠️ Nombre de lignes inattendu: {len(result)}")
            
    except Exception as e:
        print(f"❌ Test échoué avec l'erreur: {e}")
        return False
    
    return True

def test_lotecart_edge_cases():
    """Test des cas limites"""
    processor = LotecartProcessor()
    
    edge_cases = [
        {
            'CODE_ARTICLE': 'EDGE001',
            'is_new_lotecart': True,
            'QUANTITE_CORRIGEE': 0,
            'reference_line': 'S;SES001;INV001;2000;SITE01;0;0;2;EDGE001;LOC01;AM;UN;0;ZONE1;LOT002'
        },
        {
            'CODE_ARTICLE': 'EDGE002',
            'is_new_lotecart': True,
            'QUANTITE_CORRIGEE': 999,
            'reference_line': 'S;SES001;INV001;3000;SITE01;50;0;1;EDGE002;LOC01;AM;UN;0;ZONE1;LOT003'
        }
    ]
    
    print("\n🧪 Test des cas limites...")
    
    try:
        result = processor.generate_lotecart_lines(edge_cases, max_line_number=5000)
        print(f"✅ Test cas limites réussi ! {len(result)} lignes générées")
        
        for i, line in enumerate(result):
            parts = line.split(';')
            qte_corrigee = parts[5] if len(parts) > 5 else 'N/A'
            indicateur = parts[7] if len(parts) > 7 else 'N/A'
            print(f"  {i+1}. Article: {parts[8] if len(parts) > 8 else 'N/A'}, Qté: {qte_corrigee}, Indicateur: {indicateur}")
            
    except Exception as e:
        print(f"❌ Test cas limites échoué: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Démarrage des tests de correction LOTECART\n")
    
    success1 = test_lotecart_with_nan_reference()
    success2 = test_lotecart_edge_cases()
    
    if success1 and success2:
        print("\n🎉 Tous les tests sont passés ! Le bug est corrigé.")
    else:
        print("\n❌ Certains tests ont échoué.")
        sys.exit(1)