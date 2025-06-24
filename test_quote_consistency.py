#!/usr/bin/env python3
"""
Test validator untuk memverifikasi perbaikan generator quote consistency
"""

import sys
import re
from pathlib import Path

def validate_quote_consistency(feature_content, steps_content):
    """Validate that quotes in feature and step definitions match"""
    
    issues = []
    
    # Extract step text from feature file
    feature_steps = re.findall(r'(Given|When|Then|And)\s+(.+)', feature_content)
    
    # Extract step decorators from steps file
    step_decorators = re.findall(r'@(given|when|then)\([\'"](.+?)[\'"]\)', steps_content)
    
    # Create mappings
    feature_step_texts = {step[1].strip() for step in feature_steps}
    step_def_texts = {step[1].strip() for step in step_decorators}
    
    # Check for mismatches
    for feature_text in feature_step_texts:
        if feature_text not in step_def_texts:
            # Look for similar texts with different quotes
            similar_found = False
            for step_text in step_def_texts:
                if normalize_quotes(feature_text) == normalize_quotes(step_text):
                    issues.append(f"Quote mismatch: Feature has '{feature_text}' but step def has '{step_text}'")
                    similar_found = True
                    break
            
            if not similar_found:
                issues.append(f"Missing step definition for: '{feature_text}'")
    
    return issues

def normalize_quotes(text):
    """Normalize quotes for comparison"""
    return text.replace('"', "'").replace(''', "'").replace(''', "'")

def test_ccc_project():
    """Test quote consistency for CCC project"""
    print("🧪 TESTING CCC PROJECT QUOTE CONSISTENCY")
    print("=" * 50)
    
    base_path = Path(__file__).parent / "CCC"
    if not base_path.exists():
        print("❌ CCC folder not found!")
        return False
    
    feature_file = base_path / "features" / "pencarian" / "pencarian.feature"
    steps_file = base_path / "features" / "steps" / "pencarian_steps.py"
    
    print(f"📄 Feature file: {feature_file}")
    print(f"📄 Steps file: {steps_file}")
    
    if not feature_file.exists() or not steps_file.exists():
        print("❌ Files not found!")
        return False
    
    # Read files
    feature_content = feature_file.read_text(encoding='utf-8')
    steps_content = steps_file.read_text(encoding='utf-8')
    
    # Validate
    issues = validate_quote_consistency(feature_content, steps_content)
    
    if issues:
        print("❌ QUOTE CONSISTENCY ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        return False
    else:
        print("✅ PERFECT QUOTE CONSISTENCY!")
        return True

def test_zzz_project():
    """Test quote consistency for ZZZ project"""
    print("🧪 TESTING ZZZ PROJECT QUOTE CONSISTENCY")
    print("=" * 50)
    
    base_path = Path(__file__).parent / "ZZZ"
    if not base_path.exists():
        print("❌ ZZZ folder not found!")
        return False
    
    feature_file = base_path / "features" / "pencarian" / "pencarian.feature"
    steps_file = base_path / "features" / "steps" / "pencarian_steps.py"
    
    print(f"📄 Feature file: {feature_file}")
    print(f"📄 Steps file: {steps_file}")
    
    if not feature_file.exists() or not steps_file.exists():
        print("❌ Files not found!")
        return False
    
    # Read files
    feature_content = feature_file.read_text(encoding='utf-8')
    steps_content = steps_file.read_text(encoding='utf-8')
    
    # Validate
    issues = validate_quote_consistency(feature_content, steps_content)
    
    if issues:
        print("❌ QUOTE CONSISTENCY ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        return False
    else:
        print("✅ PERFECT QUOTE CONSISTENCY!")
        return True
    feature_file = base_path / "features" / "pencarian" / "pencarian.feature"
    steps_file = base_path / "features" / "steps" / "pencarian_steps.py"
    
    if not feature_file.exists() or not steps_file.exists():
        print("❌ Files not found!")
        return False
    
    # Read files
    with open(feature_file, 'r', encoding='utf-8') as f:
        feature_content = f.read()
    
    with open(steps_file, 'r', encoding='utf-8') as f:
        steps_content = f.read()
    
    # Validate
    issues = validate_quote_consistency(feature_content, steps_content)
    
    print(f"📄 Feature file: {feature_file}")
    print(f"📄 Steps file: {steps_file}")
    print()
    
    if issues:
        print("❌ QUOTE CONSISTENCY ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        return False
    else:
        print("✅ PERFECT QUOTE CONSISTENCY!")
        return True

def test_xxx_project():
    """Test quote consistency for ZZZ project (formerly xxx)"""
    print("\n🧪 TESTING ZZZ PROJECT QUOTE CONSISTENCY")
    print("=" * 50)
    
    base_path = Path(__file__).parent / "ZZZ"
    feature_file = base_path / "features" / "pencarian" / "pencarian.feature"
    steps_file = base_path / "features" / "steps" / "pencarian_steps.py"
    
    print(f"📄 Feature file: {feature_file}")
    print(f"📄 Steps file: {steps_file}")
    
    if not feature_file.exists() or not steps_file.exists():
        print("❌ Files not found!")
        return False
    
    # Read files
    with open(feature_file, 'r', encoding='utf-8') as f:
        feature_content = f.read()
    
    with open(steps_file, 'r', encoding='utf-8') as f:
        steps_content = f.read()
    
    # Validate
    issues = validate_quote_consistency(feature_content, steps_content)
    
    if issues:
        print("❌ QUOTE CONSISTENCY ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        return False
    else:
        print("✅ PERFECT QUOTE CONSISTENCY!")
        return True

def test_testx_project():
    """Test quote consistency for TestX project"""
    print("🧪 TESTING TESTX PROJECT QUOTE CONSISTENCY")
    print("=" * 50)
    
    base_path = Path(__file__).parent / "TestX"
    if not base_path.exists():
        print("❌ TestX folder not found!")
        return False
    
    feature_file = base_path / "features" / "pencarian" / "pencarian.feature"
    steps_file = base_path / "features" / "steps" / "pencarian_steps.py"
    
    print(f"📄 Feature file: {feature_file}")
    print(f"📄 Steps file: {steps_file}")
    
    if not feature_file.exists() or not steps_file.exists():
        print("❌ Files not found!")
        return False
    
    try:
        with open(feature_file, 'r', encoding='utf-8') as f:
            feature_content = f.read()
        
        with open(steps_file, 'r', encoding='utf-8') as f:
            steps_content = f.read()
        
        issues = validate_quote_consistency(feature_content, steps_content)
        
        if issues:
            print("❌ Quote consistency issues found:")
            for issue in issues:
                print(f"   • {issue}")
            return False
        else:
            print("✅ Quote consistency validation passed!")
            return True
            
    except Exception as e:
        print(f"❌ Error reading files: {e}")
        return False

def test_tesd_project():
    """Test quote consistency for tesD project"""
    print("🧪 TESTING TESD PROJECT QUOTE CONSISTENCY")
    print("=" * 50)
    
    base_path = Path(__file__).parent / "tesD"
    if not base_path.exists():
        print("❌ tesD folder not found!")
        return False
    
    feature_file = base_path / "features" / "pencarian_cemetery" / "pencarian_cemetery.feature"
    steps_file = base_path / "features" / "steps" / "pencarian_cemetery_steps.py"
    
    print(f"📄 Feature file: {feature_file}")
    print(f"📄 Steps file: {steps_file}")
    
    if not feature_file.exists() or not steps_file.exists():
        print("❌ Files not found!")
        return False
    
    try:
        with open(feature_file, 'r', encoding='utf-8') as f:
            feature_content = f.read()
        
        with open(steps_file, 'r', encoding='utf-8') as f:
            steps_content = f.read()
        
        issues = validate_quote_consistency(feature_content, steps_content)
        
        if issues:
            print("❌ Quote consistency issues found:")
            for issue in issues:
                print(f"   • {issue}")
            return False
        else:
            print("✅ Quote consistency validation passed!")
            return True
            
    except Exception as e:
        print(f"❌ Error reading files: {e}")
        return False

def test_import_statements():
    """Test that test files have proper imports"""
    print("\n🧪 TESTING IMPORT STATEMENTS")
    print("=" * 50)
    
    projects = [
        ("CCC", "pencarian"),
        ("ZZZ", "pencarian"),
        ("TestX", "pencarian"),
        ("tesD", "pencarian_cemetery")
    ]
    
    all_good = True
    
    for project, feature in projects:
        test_file = Path(__file__).parent / project / f"test_{feature}.py"
        
        if not test_file.exists():
            print(f"❌ {project}: Test file not found!")
            all_good = False
            continue
        
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if import is present
        import_pattern = f"from features.steps.{feature}_steps import \\*"
        if re.search(import_pattern, content):
            print(f"✅ {project}: Import statement found")
        else:
            print(f"❌ {project}: Missing import statement")
            all_good = False
    
    return all_good

def main():
    """Run all validation tests"""
    print("🔧 GENERATOR QUOTE CONSISTENCY VALIDATOR")
    print("=" * 60)
    
    # Test projects
    ccc_ok = test_ccc_project()
    zzz_ok = test_zzz_project()
    testx_ok = test_testx_project()
    tesd_ok = test_tesd_project()
    import_ok = test_import_statements()
    
    # Summary
    print("\n📊 VALIDATION SUMMARY:")
    print(f"CCC Project: {'✅ PASS' if ccc_ok else '❌ FAIL'}")
    print(f"ZZZ Project: {'✅ PASS' if zzz_ok else '❌ FAIL'}")
    print(f"TestX Project: {'✅ PASS' if testx_ok else '❌ FAIL'}")
    print(f"tesD Project: {'✅ PASS' if tesd_ok else '❌ FAIL'}")
    print(f"Import Statements: {'✅ PASS' if import_ok else '❌ FAIL'}")
    
    all_pass = ccc_ok and zzz_ok and testx_ok and tesd_ok and import_ok
    
    if all_pass:
        print("\n🎉 ALL VALIDATION TESTS PASSED!")
        print("Generator fixes are working correctly!")
    else:
        print("\n💥 SOME TESTS FAILED!")
        print("Generator still needs improvements.")
    
    return all_pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
