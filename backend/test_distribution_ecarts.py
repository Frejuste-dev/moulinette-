#!/usr/bin/env python3
"""
Test de la nouvelle logique de distribution des écarts FIFO/LIFO
"""
import sys
import os
sys.path.append('.')

import pandas as pd
from datetime import datetime

def test_distribution_logic():
    """Test la logique de distribution des écarts"""
    print("=== TEST DISTRIBUTION ÉCARTS FIFO/LIFO ===")
    
    # Simuler des données originales avec plusieurs lots pour un même article
    original_data = {
        'CODE_ARTICLE': ['ART001', 'ART001', 'ART001', 'ART002'],
        'NUMERO_INVENTAIRE': ['INV001', 'INV001', 'INV001', 'INV001'],
        'NUMERO_LOT': ['LOT001', 'LOT002', 'LOT003', 'LOT004'],
        'QUANTITE_ORIGINALE': [50, 30, 20, 100],  # Total ART001 = 100
        'QUANTITE_REELLE_SAISIE_TOTALE': [80, 80, 80, 95],  # Saisie ART001 = 80, ART002 = 95
        'TYPE_LOT': ['type1', 'type1', 'type2', 'type1'],
        'Date_Lot': [
            datetime(2024, 1, 1),   # LOT001 - plus ancien
            datetime(2024, 2, 1),   # LOT002 - moyen
            datetime(2024, 3, 1),   # LOT003 - plus récent
            datetime(2024, 1, 15)   # LOT004
        ]
    }
    
    discrepancies_df = pd.DataFrame(original_data)
    
    print("📊 Données d'entrée:")
    print(discrepancies_df[['CODE_ARTICLE', 'NUMERO_LOT', 'QUANTITE_ORIGINALE', 'QUANTITE_REELLE_SAISIE_TOTALE', 'Date_Lot']])
    
    # Test FIFO
    print("\n🔄 Test FIFO (First In, First Out)")
    distributed_fifo = simulate_distribution(discrepancies_df, 'FIFO')
    
    # Test LIFO  
    print("\n🔄 Test LIFO (Last In, First Out)")
    distributed_lifo = simulate_distribution(discrepancies_df, 'LIFO')

def simulate_distribution(discrepancies_df, strategy):
    """Simule la logique de distribution"""
    distributed_rows = []
    
    for (code_article, numero_inventaire), group in discrepancies_df.groupby(['CODE_ARTICLE', 'NUMERO_INVENTAIRE']):
        # Calculer l'écart total pour cet article
        quantite_originale_totale = group['QUANTITE_ORIGINALE'].sum()
        quantite_reelle_saisie = group['QUANTITE_REELLE_SAISIE_TOTALE'].iloc[0]
        ecart_total = quantite_reelle_saisie - quantite_originale_totale
        
        print(f"\n📦 Article {code_article}:")
        print(f"   Quantité originale totale: {quantite_originale_totale}")
        print(f"   Quantité réelle saisie: {quantite_reelle_saisie}")
        print(f"   Écart total: {ecart_total}")
        
        # Trier les lots selon la stratégie
        if strategy == 'FIFO':
            sorted_group = group.sort_values(['Date_Lot', 'NUMERO_LOT'], na_position='last')
            print(f"   Ordre FIFO: {list(sorted_group['NUMERO_LOT'])}")
        elif strategy == 'LIFO':
            sorted_group = group.sort_values(['Date_Lot', 'NUMERO_LOT'], ascending=[False, False], na_position='first')
            print(f"   Ordre LIFO: {list(sorted_group['NUMERO_LOT'])}")
        else:
            sorted_group = group
        
        # Distribuer l'écart sur les lots
        ecart_restant = ecart_total
        
        for _, lot_row in sorted_group.iterrows():
            quantite_originale_lot = lot_row['QUANTITE_ORIGINALE']
            
            if ecart_restant == 0:
                quantite_corrigee = quantite_originale_lot
                ajustement_lot = 0
            elif ecart_restant > 0:
                # Écart positif: ajouter du stock
                ajustement_lot = min(ecart_restant, quantite_originale_lot)
                quantite_corrigee = quantite_originale_lot + ajustement_lot
                ecart_restant -= ajustement_lot
            else:
                # Écart négatif: retirer du stock
                if abs(ecart_restant) >= quantite_originale_lot:
                    quantite_corrigee = 0
                    ajustement_lot = -quantite_originale_lot
                    ecart_restant += quantite_originale_lot
                else:
                    quantite_corrigee = quantite_originale_lot + ecart_restant
                    ajustement_lot = ecart_restant
                    ecart_restant = 0
            
            print(f"   {lot_row['NUMERO_LOT']}: {quantite_originale_lot} → {quantite_corrigee} (ajust: {ajustement_lot:+})")
            
            # Créer la ligne distribuée
            distributed_row = lot_row.copy()
            distributed_row['AJUSTEMENT'] = ajustement_lot
            distributed_row['QUANTITE_CORRIGEE'] = quantite_corrigee
            distributed_rows.append(distributed_row)
        
        print(f"   Écart restant: {ecart_restant}")
    
    return pd.DataFrame(distributed_rows)

if __name__ == "__main__":
    test_distribution_logic()