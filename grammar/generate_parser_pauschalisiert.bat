@echo off
REM ANTLR Parser Generator Script for SMEL_Pauschalisiert.g4
REM Run this script from the grammar/ directory

cd /d "%~dp0"

echo Generating ANTLR parser from SMEL_Pauschalisiert.g4...
java -jar antlr-4.13.2-complete.jar -Dlanguage=Python3 -visitor -o pauschalisiert SMEL_Pauschalisiert.g4

if %ERRORLEVEL% == 0 (
    echo Done! SMEL_Pauschalisiert parser files generated in pauschalisiert/ directory.
    echo Files created:
    echo   - pauschalisiert/SMEL_PauschalisiertLexer.py
    echo   - pauschalisiert/SMEL_PauschalisiertParser.py
    echo   - pauschalisiert/SMEL_PauschalisiertListener.py
    echo   - pauschalisiert/SMEL_PauschalisiertVisitor.py
) else (
    echo Error generating parser!
    exit /b 1
)
