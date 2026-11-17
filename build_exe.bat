@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   Membangun AplikasiPenilaianPraktikum.exe
echo ============================================
echo.
echo [1/2] Memasang dependensi ...
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto gagal
echo.
echo [2/2] Membungkus menjadi .exe ...
python -m PyInstaller --noconfirm --clean AplikasiPenilaianPraktikum.spec
if errorlevel 1 goto gagal
echo.
echo Selesai! Hasil: dist\AplikasiPenilaianPraktikum.exe
pause
exit /b 0
:gagal
echo.
echo Terjadi kesalahan. Periksa pesan di atas.
pause
exit /b 1
