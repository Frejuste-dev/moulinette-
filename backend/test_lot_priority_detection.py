#!/usr/bin/env python3
"""
Test de la nouvelle logique de détection des lots priorité 1
"""
import sys
import os
sys.path.append('.')

from services.file_processor import FileProcessorService
from services.config_service import config_service
from datetime import datetime

def test_priority1_lot_detection():
    """Test la détection des lots priorité 1 avec la nouvelle logique"""
    print("=== TEST DÉTECTION LOTS PRIORITÉ 1 ===")
    print()
    
    # Initialiser le service
    processor = FileProcessorService()
    
    # Cas de test avec différents formats de lots
    test_cases = [
        # Lots priorité 1 valides (5 chars + DDMMYY + 4 chars)
        {
            "lot": "CPKU1070725ABCD",
            "expected_type": "type1",
            "expected_date": datetime(2025, 7, 7),
            "description": "Lot CPKU1 valide"
        },
        {
            "lot": "CB2TV020425WXYZ", 
            "expected_type": "type1",
            "expected_date": datetime(2025, 4, 2),
            "description": "Lot CB2TV valide"
        },
        {
            "lot": "SBAMA311224EFGH",
            "expected_type": "type1", 
            "expected_date": datetime(2024, 12, 31),
            "description": "Lot SBAMA valide"
        },
        
        # Lots priorité 2 (LOT + date)
        {
            "lot": "LOT311224",
            "expected_type": "type2",
            "expected_date": datetime(2024, 12, 31),
            "description": "Lot type 2 valide"
        },
        
        # Lots avec codes de site non reconnus
        {
            "lot": "XXXXX070725ABCD",
            "expected_type": "unknown",
            "expected_date": None,
            "description": "Code site non reconnu"
        },
        
        # Lots avec format incorrect
        {
            "lot": "CPKU070725",  # Manque les 4 derniers caractères
            "expected_type": "unknown",
            "expected_date": None,
            "description": "Format incomplet"
        },
        {
            "lot": "CPKU1070725ABCDE",  # Trop de caractères à la fin
            "expected_type": "unknown", 
            "expected_date": None,
            "description": "Format trop long"
        },
        
        # Lots avec dates invalides
        {
            "lot": "CPKU1320425ABCD",  # 32ème jour
            "expected_type": "type1",
            "expected_date": None,
            "description": "Date invalide (jour 32)"
        },
        {
            "lot": "CPKU1071325ABCD",  # 13ème mois
            "expected_type": "type1", 
            "expected_date": None,
            "description": "Date invalide (mois 13)"
        }
    ]
    
    print(f"Configuration chargée:")
    print(f"  - Pattern type 1: {processor.LOT_PATTERNS['type1']}")
    print(f"  - Codes de site priorité 1: {len(processor.PRIORITY1_SITE_CODES)} codes")
    print(f"  - Exemples de codes: {list(processor.PRIORITY1_SITE_CODES)[:5]}...")
    print()
    
    all_passed = True
    
    for i, case in enumerate(test_cases, 1):
        lot_number = case["lot"]
        expected_type = case["expected_type"]
        expected_date = case["expected_date"]
        description = case["description"]
        
        print(f"Test {i:2d}: {description}")
        print(f"         Lot: {lot_number}")
        
        # Tester la détection
        detected_date, detected_type = processor._extract_date_from_lot(lot_number)
        
        # Vérifier le type
        type_ok = detected_type == expected_type
        
        # Vérifier la date
        if expected_date is None:
            date_ok = detected_date is None
        else:
            date_ok = (detected_date is not None and 
                      detected_date.day == expected_date.day and
                      detected_date.month == expected_date.month and
                      detected_date.year == expected_date.year)
        
        status = "✅ PASS" if (type_ok and date_ok) else "❌ FAIL"
        
        print(f"         Type détecté: {detected_type} (attendu: {expected_type}) {'✅' if type_ok else '❌'}")
        if detected_date:
            print(f"         Date détectée: {detected_date.strftime('%d/%m/%Y')} (attendu: {expected_date.strftime('%d/%m/%Y') if expected_date else 'None'}) {'✅' if date_ok else '❌'}")
        else:
            print(f"         Date détectée: None (attendu: {expected_date.strftime('%d/%m/%Y') if expected_date else 'None'}) {'✅' if date_ok else '❌'}")
        print(f"         Résultat: {status}")
        print()
        
        if not (type_ok and date_ok):
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ La nouvelle logique de détection des lots priorité 1 fonctionne correctement")
        print("✅ Les 5 caractères de site sont correctement validés")
        print("✅ Les dates sont correctement extraites")
        print("✅ Les formats invalides sont correctement rejetés")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ!")
        print("⚠️ La logique de détection nécessite des corrections")
    
    return all_passed

def test_site_code_validation():
    """Test spécifique de la validation des codes de site"""
    print("\n=== TEST VALIDATION CODES DE SITE ===")
    
    processor = FileProcessorService()
    
    # Tester quelques codes de la liste
    valid_codes = ['CPKU1', 'CB2TV', 'SBAMA', 'CANCB', 'CYKTV']
    invalid_codes = ['CPKU', 'INVALID', 'TEST1', 'ABCDE']
    
    print("Codes valides:")
    for code in valid_codes:
        is_valid = code in processor.PRIORITY1_SITE_CODES
        status = "✅" if is_valid else "❌"
        print(f"  {status} {code}")
    
    print("\nCodes invalides:")
    for code in invalid_codes:
        is_valid = code in processor.PRIORITY1_SITE_CODES
        status = "❌" if not is_valid else "⚠️"
        print(f"  {status} {code}")

if __name__ == "__main__":
    print("🚀 Test de la nouvelle logique des lots priorité 1")
    print("📋 Format: 5 caractères site + DDMMYY + 4 caractères")
    print()
    
    success1 = test_priority1_lot_detection()
    test_site_code_validation()
    
    if success1:
        print("\n🎉 Configuration mise à jour avec succès!")
        print("📝 Les lots priorité 1 sont maintenant correctement détectés")
    else:
        print("\n❌ Des problèmes ont été détectés dans la configuration")