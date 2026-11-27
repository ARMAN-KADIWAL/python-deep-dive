# Naming Improvements Made During Refactoring

## Variable Names

### Before (Poor Names)
- `x, y, z` - Generic, meaningless parameter names
- `op` - Abbreviated, unclear
- `data` - Too generic
- `max_val, min_val` - Abbreviated unnecessarily

### After (Meaningful Names)
- `first_number, second_number, third_number` - Clear purpose
- `operation` - Full word, self-explanatory
- `sample_data, numbers` - Context-specific
- `maximum_value, minimum_value` - Complete, descriptive

## Function Names

### Before (Unclear Purpose)
- `calc()` - What kind of calculation?
- `process_data()` - Process how?

### After (Clear Intent)
- `perform_calculation()` - Clearly states what it does
- `calculate_statistics()` - Specific about the processing
- `find_extreme_value()` - Describes the search operation

## Class Names

### Added in Final Version
- `Calculator` - Clear responsibility
- `DataProcessor` - Specific purpose
- `CalculationError` - Custom exception with clear meaning

## Benefits of Good Naming

1. **Self-Documenting Code**: Names explain what the code does
2. **Easier Maintenance**: Future developers understand the purpose
3. **Reduced Comments**: Good names reduce need for explanatory comments
4. **Better Debugging**: Clear names make error tracking easier
