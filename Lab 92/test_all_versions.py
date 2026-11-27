# Test script to verify all versions work correctly
import subprocess
import sys

def run_script(script_name):
    """Run a Python script and return its output."""
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Script timed out"
    except FileNotFoundError:
        return False, "", f"File {script_name} not found"

def test_all_scripts():
    """Test all refactored scripts."""
    scripts = [
        "messy_calculator.py",
        "clean_calculator.py", 
        "dry_calculator.py",
        "final_clean_calculator.py"
    ]
    
    print("Testing All Refactored Versions:")
    print("=" * 40)
    
    for script in scripts:
        success, stdout, stderr = run_script(script)
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{script}: {status}")
        
        if not success and stderr:
            print(f"  Error: {stderr.strip()}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    test_all_scripts()
