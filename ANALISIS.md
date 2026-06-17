# Análisis de PortfolioAR — Diagnóstico y hoja de ruta de arreglos

> Documento de diagnóstico generado para usar como guía al reparar el proyecto.
> Proyecto: Django 4.2, arquitectura 3 capas (`views` → `business` → `data_access`).
> Estado actual: **no arranca**. Hay bugs bloqueantes, vulnerabilidades y funcionalidad simulada.

## TL;DR

La arquitectura en capas está bien y es lo más valioso del TP. Pero el proyecto hoy no
corre por 4 bugs bloqueantes, las vistas tienen un IDOR (acceso a datos de otros usuarios),
y los "diferenciales" del README (S&P 500, análisis técnico, IA) están hardcodeados, no
implementados. Orden sugerido de trabajo: primero los 4 bloqueantes para que levante,
después seguridad y lógica, y al final decidir qué hacer con lo simulado.

---

## 1. Bugs bloqueantes (impiden que el proyecto corra)

### 1.1 Falta `AUTH_USER_MODEL` en `settings.py`
- **Síntoma:** `makemigrations` falla con clash de accessors (`auth.User` vs `core.User`).
- **Causa:** hay un `User` custom en `core/models.py` que hereda de `AbstractUser`, pero
  `settings.py` nunca declara el modelo de usuario.
- **Fix:** agregar en `settings.py`:
  ```python
  AUTH_USER_MODEL = 'core.User'
  ```

### 1.2 No hay migraciones
- **Síntoma:** no se puede `migrate`.
- **Causa:** solo existen los `__init__.py` en cada carpeta `migrations/`.
- **Fix:** tras resolver 1.1, generar y commitear migraciones:
  ```bash
  python manage.py makemigrations core portfolio alerts
  ```

### 1.3 Bug de namespaces en las URLs de autenticación
- **Síntoma:** `NoReverseMatch` en casi todas las páginas (navbar `base.html`, login,
  register, profile, change_password) y en los `redirect()` de `core/views.py`.
- **Causa:** las vistas de auth están en `core/urls_auth.py`, que **no tiene `app_name`**, y
  se incluye en `portfolioar/urls.py` bajo `auth/` **sin namespace**. Pero los templates y
  vistas usan `core:login`, `core:register`, `core:logout`, `core:profile`,
  `core:change_password`. El namespace `core` solo conoce `home`.
- **Fix (una opción):** mover las rutas de auth a `core/urls.py` (que ya tiene
  `app_name = 'core'`), o agregar `app_name = 'core'` en `urls_auth.py` e incluirlo con
  `namespace='core'`. Cuidado de no duplicar el namespace `core` en dos includes.

### 1.4 `get_stock_by_sector` no está importado
- **Síntoma:** `NameError` si se llama a `StockManager.get_by_sector()`.
- **Causa:** `core/business.py` usa `get_stock_by_sector(sector_id)` pero no lo importa
  (sí importa el resto de funciones de `data_access`).
- **Fix:** agregarlo al import desde `core/data_access.py`.

---

## 2. Seguridad

### 2.1 IDOR — acceso a datos de otros usuarios (importante)
- **Síntoma:** cualquier usuario logueado puede ver/editar/borrar posiciones, órdenes y
  alertas de otros cambiando el ID en la URL.
- **Causa:** las vistas de `portfolio` y `alerts` buscan por ID sin filtrar por
  `request.user`. Ej.: `position_detail`, `position_delete`, `alert_delete`,
  `order_delete` hacen `get_*_by_id(id)` directo.
- **Fix:** filtrar siempre por dueño, p. ej. `get_object_or_404(Position, id=..., user=request.user)`,
  o agregar el filtro de `user` en la capa `data_access`/`business`.

### 2.2 Configuración insegura por defecto (aceptable para TP, mencionar)
- `SECRET_KEY` con default `django-insecure-...`.
- `DEBUG=True` por defecto.
- `ALLOWED_HOSTS='*'` por defecto.
- El `.env` está en `.gitignore` y solo tiene placeholders (sin secretos filtrados). OK.

---

## 3. Errores de lógica

### 3.1 El profit/loss siempre da 0
- En `PortfolioManager.calculate_position_performance()` se hace
  `current_price_usd = position.stock_price_usd` (el precio de compra), entonces
  `current_value == invested_amount` y la ganancia siempre es 0. Ni siquiera usa el
  precio "actual" simulado.

### 3.2 Mezcla de unidades en el resumen del portfolio
- En `calculate_portfolio_summary()` `total_invested` usa `stock_price_local` (pesos) y
  `total_current_value` usa `stock_price_usd` (dólares). El % de ganancia compara pesos
  contra dólares — sin sentido. Definir una sola moneda de referencia.

### 3.3 Cálculo de inflación INDEC conceptualmente mal
- `ExternalAPIs.get_indec_inflation()` llama a la API de datos.gob.ar pero devuelve el
  **nivel del índice**, no la **variación porcentual** entre las dos fechas. Hay que tomar
  el índice en `start_date` y en `end_date` y calcular el % de variación.

---

## 4. Funcionalidad simulada (no implementada)

El README la vende como "diferencial clave", pero hoy está hardcodeada:

- `get_sp500_performance()` → siempre `Decimal('10.5')`.
- `get_current_price()` → siempre `150.00`.
- `get_technical_indicators()` → RSI/MACD/SMA fijos inventados.
- **LangChain / OpenAI / pandas-ta** están en `requirements.txt` pero no se usan en ningún
  `.py` (solo aparecen en `setup.py`). La "recomendación IA" es solo un `TextField` vacío.
- No hay evaluación periódica de alertas wireada en ningún lado (no hay scheduler/cron).

**Decisión a tomar:** o se implementan de verdad (APIs reales de IOL/precios, pandas-ta
para indicadores, LangChain para la recomendación), o se ajusta el README para no prometer
lo que es stub. Para un TP, ser explícito sobre qué es simulado suele ser mejor que
aparentar.

---

## 5. Tests

- `tests.py` tiene buena cobertura de modelos y managers, pero probablemente **no pasan**:
  usan `User.objects.create_user(first_name=..., email=...)` sin `username`, y el
  `UserManager` por defecto exige `username`. Sumado al problema 1.1, la suite no corre.
- Está en la raíz con `django.setup()` manual, en vez de seguir la convención `app/tests.py`
  esperada por `pytest-django` / `manage.py test`.
- **Fix:** crear un `UserManager` custom basado en email, o ajustar los tests para pasar
  `username`; y mover/partir los tests por app.

---

## 6. Entorno de desarrollo en Mac (SQLite)

- `settings.py` asume SQL Server + ODBC Driver 17, incómodo en Mac.
- **Fix sugerido:** switch por variable de entorno para usar SQLite en desarrollo:
  ```python
  if os.environ.get('USE_SQLITE') == 'True':
      DATABASES['default'] = {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': BASE_DIR / 'db.sqlite3',
      }
  ```
  Luego: `USE_SQLITE=True python manage.py migrate`.

---

## 7. Lo que está bien (no tocar / conservar)

- Separación en capas consistente y prolija en las tres apps.
- Modelos bien diseñados: FKs, `related_name`, `db_table`, `verbose_name` en español,
  M2M de condiciones de alerta.
- Admin de Django customizado (`CustomUserAdmin`, etc.).
- Tooling serio para un TP: `flake8`, `black`, `isort`, `mypy`, `pre-commit`, `tox`,
  Docker, nginx, y CI con matriz de Python (3.8–3.11).

---

## 8. Orden de ejecución sugerido

1. `AUTH_USER_MODEL = 'core.User'` (1.1)
2. Arreglar namespaces de URLs de auth (1.3)
3. Import de `get_stock_by_sector` (1.4)
4. Switch a SQLite para dev (6) + generar migraciones (1.2)
5. Verificar que levante: `migrate`, `createsuperuser`, `runserver`, navegar las páginas
6. IDOR: filtrar por `request.user` en todas las vistas (2.1)
7. Lógica: profit/loss, unidades del resumen, inflación (3.1–3.3)
8. Tests: arreglar `create_user` / `UserManager` (5)
9. Decidir qué hacer con lo simulado: implementar o documentar como stub (4)

> Sugerencia de flujo de trabajo: un commit por cada punto arreglado, así queda el
> historial de cambios trackeado y se puede volver atrás si algo rompe.
