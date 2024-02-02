# IconDLL

A tool to compile multiply icons into single dll.

## Development

1. Open `Developer PowerShell` from  **Windows Start menu**.
2. Setup python virtual environments:
   ```powershell
   python -m venv .venv
   ```
3. Active python virtual environment:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
4. Install python dependency:
   ```powershell
   pip install -r requirements.txt
   ```
5. Run program:
   ```powershell
   python .\main.py
   ```

To generate python dependency:

```powershell
pip freeze > requirements.txt
```

## Third_party

+ [svg_to_ico](https://github.com/Ortham/svg_to_ico)
