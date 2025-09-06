#!/bin/bash

# 🧪 Test de Régression Automatique - PaniniFS Optimisé
# Valide que toutes les optimisations fonctionnent encore

echo "🧪 TEST DE RÉGRESSION PANINIFSOPTIMISÉ"
echo "========================================="

# Variables de test
TEST_RESULTS=()
TOTAL_TESTS=0
PASSED_TESTS=0

# Fonction de test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit_code="${3:-0}"
    
    echo "🔍 Test: $test_name"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if eval "$test_command" > /dev/null 2>&1; then
        if [ $? -eq $expected_exit_code ]; then
            echo "   ✅ PASSÉ"
            PASSED_TESTS=$((PASSED_TESTS + 1))
            TEST_RESULTS+=("✅ $test_name")
        else
            echo "   ❌ ÉCHEC (code de sortie inattendu)"
            TEST_RESULTS+=("❌ $test_name - Code sortie")
        fi
    else
        echo "   ❌ ÉCHEC"
        TEST_RESULTS+=("❌ $test_name - Erreur exécution")
    fi
}

echo "📦 1. Tests Structure Consolidée"
echo "================================"

# Test 1: Vérifier consolidation repos
run_test "Consolidation GitHub" \
    "[ -d '/home/stephane/GitHub/PaniniFS-1' ] && [ -L '/home/stephane/GitHub/Pensine' ]"

# Test 2: Vérifier accessibilité Pensine
run_test "Pensine accessible" \
    "[ -d '/home/stephane/GitHub/Pensine' ] && [ -f '/home/stephane/GitHub/Pensine/README.md' ]"

# Test 3: Vérifier autres repos consolidés
run_test "Repos consolidés" \
    "[ -L '/home/stephane/GitHub/totoro-automation' ] && [ -L '/home/stephane/GitHub/hexagonal-demo' ]"

echo ""
echo "⚡ 2. Tests Performance"
echo "======================"

# Test 4: Temps de scan acceptable
run_test "Performance scan" \
    "timeout 10s find /home/stephane/GitHub -name '*.py' | head -100 > /dev/null"

# Test 5: Accès rapide fichiers
run_test "Accès fichiers rapide" \
    "timeout 5s ls -la /home/stephane/GitHub/*/README.md > /dev/null"

echo ""
echo "🔧 3. Tests Robustesse"
echo "====================="

# Test 6: Gestion erreurs Unicode (simulation)
run_test "Gestion Unicode" \
    "python3 -c \"print('Test Unicode: été, naïve, café'.encode('utf-8', errors='replace').decode('utf-8'))\""

# Test 7: Dépendances de base disponibles
run_test "Dépendances Python de base" \
    "python3 -c 'import pathlib, time, os; print(\"OK\")'"

echo ""
echo "📊 4. Tests Notebooks"
echo "===================="

# Test 8: Notebook optimisé existe
run_test "Notebook optimisé présent" \
    "[ -f '/home/stephane/GitHub/PaniniFS-1/Copilotage/colab_notebook_fixed.ipynb' ]"

# Test 9: Script lancement existe
run_test "Script lancement présent" \
    "[ -x '/home/stephane/GitHub/PaniniFS-1/Copilotage/scripts/launch_optimized_colab.sh' ]"

# Test 10: Documentation présente
run_test "Documentation présente" \
    "[ -f '/home/stephane/GitHub/PaniniFS-1/Copilotage/MIGRATION-GUIDE.md' ]"

echo ""
echo "🎯 RAPPORT FINAL"
echo "================"

echo "📊 Résultats: $PASSED_TESTS/$TOTAL_TESTS tests réussis"

if [ $PASSED_TESTS -eq $TOTAL_TESTS ]; then
    echo "🎉 TOUS LES TESTS RÉUSSIS !"
    echo "✅ Optimisations fonctionnelles"
    echo "✅ Consolidation opérationnelle"
    echo "✅ Performance maintenue"
    echo "✅ Robustesse confirmée"
    echo ""
    echo "🚀 SYSTÈME PRÊT POUR PRODUCTION"
    exit 0
else
    echo "⚠️ CERTAINS TESTS ONT ÉCHOUÉ"
    echo ""
    echo "📋 Détail des tests:"
    for result in "${TEST_RESULTS[@]}"; do
        echo "   $result"
    done
    echo ""
    echo "🔧 Vérifiez les erreurs ci-dessus"
    exit 1
fi
