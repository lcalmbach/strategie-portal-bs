# gsp-controlling

## Einführung
Diese Django-Applikation erlaubt die Erfassung von Rückmeldungen zum Gleichstellungsplan. 

## Konfiguration Server

### Verzeichnisse
App: E:\app_install\web\gsp-controlling-app\src
venv: E:\app_install\virtualenvs\django_venv_3_12_3
requiremetns.txt: E:\app_install\virtualenvs\requirements_django_venv_3_12_3.txt

### Scheduler Einstellungen
- täglich Neustart, 7:00
- action: 
  - program: requirements_django_venv_3_12_3.txt
  - parameters: requirements_django_venv_3_12_3.txt
  - start in: E:\app_install\web\gsp-controlling-app\src