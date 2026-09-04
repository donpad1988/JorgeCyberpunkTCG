# P0.3 — PROCEDIMIENTO OPERACIONAL DE BACKUP Y RECUPERACIÓN SQLITE

**Proyecto:** JorgeCyberpunkTCG  
**Entorno de Producción:** PythonAnywhere (`jorgecyberpunktcg`)  
**Base de datos:** SQLite (`db.sqlite3`)  
**Estado:** IMPLEMENTACIÓN LOCAL COMPLETADA / VALIDACIÓN PRODUCCIÓN PENDIENTE  

---

## 1. OBJETIVO

Establecer un procedimiento operacional seguro, simple, reproducible y automatizable para la creación de copias de seguridad de la base de datos SQLite en producción, verificación de su integridad, rotación de archivos rutinarios y restauración rápida ante incidentes o fallos en despliegues.

---

## 2. ARQUITECTURA DEL SISTEMA DE BACKUP

El sistema utiliza el script standalone `scripts/backup_sqlite.py`, desarrollado con la librería estándar de Python (`sqlite3`, `pathlib`, `argparse`, `datetime`).

*   **Sin dependencias externas:** No requiere Django activado ni paquetes instalados vía `pip`.
*   **Agnóstico del binario CLI `sqlite3`:** Utiliza la API nativa `sqlite3.Connection.backup()`, garantizando disponibilidad en cualquier entorno Python 3.13.
*   **Consistencia en caliente (*Online Backup API*):** Adquiere bloqueos de lectura graduados página por página. Es 100% transaccional y seguro incluso ante lecturas/escrituras concurrentes.

---

## 3. UBICACIÓN Y ESTRUCTURA DE DIRECTORIOS EN PRODUCCIÓN

En PythonAnywhere (`/home/jorgecyberpunktcg`):

*   **Base de Datos Activa:**  
    `/home/jorgecyberpunktcg/JorgeCyberpunkTCG/db.sqlite3`
*   **Directorio de Respaldo (FUERA DEL REPOSICIONARIO):**  
    `/home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG/`

> **Regla de Seguridad:** El directorio de respaldos se ubica **fuera** del directorio del repositorio de Git para prevenir la inclusión accidental de datos sensibles en el control de versiones y proteger las copias ante comandos destructivos de Git (`git clean -fdx`).

---

## 4. NOMENCLATURA DE ARCHIVOS

1.  **Backups Rutinarios (Sin etiqueta):**  
    `db_backup_YYYYMMDD_HHMMSS.sqlite3`  
    *Ejemplo:* `db_backup_20260904_153000.sqlite3`
2.  **Backups de Hito / Pre-Deploy (Con etiqueta `--label`):**  
    `db_backup_<label_sanitizada>_YYYYMMDD_HHMMSS.sqlite3`  
    *Ejemplo:* `db_backup_pre_P0.2_20260904_153000.sqlite3`

Las etiquetas se sanitizan automáticamente para permitir únicamente caracteres alfanuméricos, guiones y guiones bajos (`[a-zA-Z0-9_-]`), previniendo inyecciones de rutas o caracteres no válidos.

---

## 5. COMANDOS DE EJECUCIÓN

### A. Crear un backup rutinario (con rotación de los 10 más recientes)
```bash
python scripts/backup_sqlite.py \
  --source /home/jorgecyberpunktcg/JorgeCyberpunkTCG/db.sqlite3 \
  --destination-dir /home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG
```

### B. Crear un backup de hito previo a un despliegue (Protegido de la rotación)
```bash
python scripts/backup_sqlite.py \
  --source /home/jorgecyberpunktcg/JorgeCyberpunkTCG/db.sqlite3 \
  --destination-dir /home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG \
  --label pre_P0.2
```

### C. Verificar únicamente la integridad de una copia existente (sin crear backup)
```bash
python scripts/backup_sqlite.py \
  --verify /home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG/db_backup_pre_P0.2_20260904_153000.sqlite3
```

---

## 6. POLÍTICA DE ROTACIÓN Y RETENCIÓN

*   **Backups Rutinarios:** El script mantiene por defecto las **10 copias rutinarias más recientes** (modificable con `--keep N`). Las copias antiguas se eliminan automáticamente tras verificar el éxito del nuevo respaldo.
*   **Backups Etiquetados (Hitos / Pre-Deploy):** Las copias con `--label` (ej. `pre_P0.2`, `pre_migration`) **NO** participan en la rotación y son preservadas indefinidamente hasta su revisión o borrado manual.

---

## 7. PERMISOS DE ARCHIVOS Y DIRECTORIOS

En entornos POSIX (Linux / PythonAnywhere):
*   **Directorio de respaldos:** Creado con permisos `0700` (`rwx------`), accesible únicamente por el usuario `jorgecyberpunktcg`.
*   **Archivos de respaldo `.sqlite3`:** Asignados con permisos `0600` (`rw-------`).

---

## 8. PROCEDIMIENTO OPERACIONAL DE RECUPERACIÓN (RECOVERY)

En caso de fallo crítico en producción, seguir estrictamente estos pasos:

1.  **Identificar el respaldo seguro:**  
    Seleccionar en `/home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG/` el archivo `.sqlite3` verificado al que se desea retornar.
2.  **Verificar integridad del respaldo antes de usarlo:**
    ```bash
    python scripts/backup_sqlite.py --verify /home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG/<backup_elegido>.sqlite3
    ```
3.  **Pausar/Acceder en ventana inactiva:**  
    Confirmar que no existen solicitudes activas de escritura.
4.  **SNAPSHOT PREVENTIVO OBLIGATORIO (`before_restore`):**  
    Antes de modificar o sobreescribir la base activa dañada, crear un respaldo de seguridad del estado actual:
    ```bash
    cp /home/jorgecyberpunktcg/JorgeCyberpunkTCG/db.sqlite3 /home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG/db.sqlite3.before_restore_$(date +%Y%m%d_%H%M%S)
    ```
5.  **Inspeccionar y preservar permisos de la base activa:**  
    Verificar los permisos del archivo activo previo a la sustitución.
6.  **Restaurar el respaldo:**
    ```bash
    cp /home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG/<backup_elegido>.sqlite3 /home/jorgecyberpunktcg/JorgeCyberpunkTCG/db.sqlite3
    ```
7.  **Asegurar permisos de archivo:**
    ```bash
    chmod 644 /home/jorgecyberpunktcg/JorgeCyberpunkTCG/db.sqlite3
    ```
8.  **Verificar integridad de la base restaurada:**
    ```bash
    python scripts/backup_sqlite.py --verify /home/jorgecyberpunktcg/JorgeCyberpunkTCG/db.sqlite3
    ```
9.  **Ejecutar Django Check:**
    ```bash
    cd /home/jorgecyberpunktcg/JorgeCyberpunkTCG
    python manage.py check --settings=config.settings.production
    ```
10. **Reiniciar la Aplicación Web (Reload):**
    ```bash
    touch /var/www/jorgecyberpunktcg_pythonanywhere_com_wsgi.py
    ```
11. **Validación post-recuperación:**
    *   Probar Endpoint de Salud: GET `https://jorgecyberpunktcg.pythonanywhere.com/health/`
    *   Verificar login/administrador si aplica.

---

## 9. PROCEDIMIENTO ESPECÍFICO DE DESPLIEGUE PARA P0.2

Procedimiento que se ejecutará en PythonAnywhere para aplicar el cambio P0.2 (Privacidad y Transparencia):

1.  **Iniciar sesión en PythonAnywhere Bash Console.**
2.  **Navegar al proyecto:**
    ```bash
    cd /home/jorgecyberpunktcg/JorgeCyberpunkTCG
    ```
3.  **Confirmar estado del repositorio:** `git status` (debe estar clean).
4.  **Ejecutar backup Pre-Deploy (P0.3):**
    ```bash
    python scripts/backup_sqlite.py \
      --source db.sqlite3 \
      --destination-dir /home/jorgecyberpunktcg/backups/JorgeCyberpunkTCG \
      --label pre_P0.2
    ```
5.  **Verificar éxito del backup (debe responder `VERIFICATION SUCCESSFUL: ok`).**
6.  **Descargar código de GitHub:**
    ```bash
    git pull origin main
    ```
7.  **Verificar migraciones:** `python manage.py showmigrations --settings=config.settings.production` (Confirmar que P0.2 no trae migraciones).
8.  **Recopilar archivos estáticos (`collectstatic`):** P0.2 actualiza hojas de estilo CSS (`components.css`, `accounts.css`):
    ```bash
    python manage.py collectstatic --noinput --settings=config.settings.production
    ```
9.  **Reload de la Aplicación Web:**
    ```bash
    touch /var/www/jorgecyberpunktcg_pythonanywhere_com_wsgi.py
    ```
10. **Verificación de URLs en producción (Rutas Reales):**
    *   Página Principal: `https://jorgecyberpunktcg.pythonanywhere.com/`
    *   Política de Privacidad: `https://jorgecyberpunktcg.pythonanywhere.com/privacidad/`
    *   Términos de Uso: `https://jorgecyberpunktcg.pythonanywhere.com/terminos/`
    *   Endpoint de Salud: `https://jorgecyberpunktcg.pythonanywhere.com/health/`
11. **Revisar Error Logs:** `/var/log/jorgecyberpunktcg.pythonanywhere.com.error.log`

---

## 10. SEGURIDAD Y PRIVACIDAD

*   Los backups de producción contienen datos personales de usuarios (emails, hashes de contraseñas de Django, mazos).
*   **Prohibiciones:**
    *   NUNCA almacenar backups dentro de `static/` ni `media/`.
    *   NUNCA exponer backups via servidor web HTTP.
    *   NUNCA commitear archivos `.sqlite3` en Git.
    *   NUNCA imprimir o volcar contenido de tablas en logs de salida del script de backup.

---

## 11. TROUBLESHOOTING

| Síntoma | Causa Probable | Solución Operacional |
| :--- | :--- | :--- |
| `Source database does not exist` | Ruta `--source` incorrecta. | Comprobar con `ls -la` la ubicación de `db.sqlite3`. |
| `Integrity check failed` | Corrupción previa o fallo durante la escritura. | El backup no se declara exitoso. Ejecutar integrity check en la fuente; de persistir, revisar logs del SO. |
| `Permission denied` al crear backup | Permisos insuficientes en `--destination-dir`. | Verificar ownership y permisos (`chmod u+rwx`). |
| Django error 500 tras restore | Permisos del archivo `db.sqlite3` o WSGI no reiniciado. | Ejecutar `chmod 644 db.sqlite3` y hacer `touch ...wsgi.py`. |

---

## 12. CRITERIO DE ACEPTACIÓN

P0.3B se considera completado localmente al cumplir:
*   [x] Script `scripts/backup_sqlite.py` creado con `sqlite3.Connection.backup()`.
*   [x] Soporte para `--source`, `--destination-dir`, `--label`, `--keep`, `--verify`.
*   [x] Verificación automática con `PRAGMA integrity_check;`.
*   [x] Rotación limpia conservando 10 rutinarios y preservando backups etiquetados.
*   [x] Tests unitarios en `apps/core/tests/test_backup_sqlite.py` pasando con éxito (13 tests OK, incluyendo simulación de recuperación).
*   [x] `.gitignore` actualizado con `db_backup_*.sqlite3` y `backups/`.
*   [x] Documentación operacional elaborada.
