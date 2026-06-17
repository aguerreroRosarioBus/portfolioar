# PortfolioAR

Sistema de gestión de inversiones para inversores argentinos que operan en mercados de acciones y bonos locales e internacionales a través de CEDEARs.

## Descripción

PortfolioAR permite gestionar la cartera de inversiones de forma centralizada, obteniendo métricas reales de rendimiento, análisis técnico automatizado y alertas configurables basadas en indicadores financieros.

El diferencial clave del sistema es contextualizar el rendimiento de cada inversión comparándolo contra el índice S&P 500 y contra la inflación argentina oficial del mismo periodo.

## Requisitos

- Python 3.8 o superior
- SQL Server
- pip

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/portfolioar.git
cd portfolioar
```

2. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. Ejecutar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Ejecutar servidor:
```bash
python manage.py runserver
```

## Arquitectura

El sistema sigue una arquitectura de 3 capas:

- **Capa de Presentación**: Django Templates y Views
- **Capa de Negocio**: Lógica de portfolio, alertas, cálculos, análisis de IA
- **Capa de Datos**: Django ORM + mssql-django + APIs externas (IOL, INDEC)

## Estructura del Proyecto

```
portfolioar/
├── core/                    # Autenticación y modelos base
│   ├── admin.py
│   ├── apps.py
│   ├── business.py
│   ├── data_access.py
│   ├── models.py
│   ├── urls.py
│   ├── urls_auth.py
│   └── views.py
├── portfolio/               # Gestión de posiciones y órdenes
│   ├── admin.py
│   ├── apps.py
│   ├── business.py
│   ├── data_access.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── alerts/                  # Sistema de alertas técnicas
│   ├── admin.py
│   ├── apps.py
│   ├── business.py
│   ├── data_access.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/               # Templates HTML
│   ├── base.html
│   ├── core/
│   ├── portfolio/
│   └── alerts/
├── portfolioar/             # Configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── .env.example
```

## Funcionalidades

### Módulo 1 – Gestión de Portfolio
- Registro de operaciones de compra y venta
- Cálculo de rendimiento de posiciones
- Comparación contra S&P 500
- Comparación contra inflación del INDEC
- Métricas del portfolio completo

### Módulo 2 – Alertas
- Configuración de alertas basadas en indicadores técnicos
- Evaluación periódica de condiciones
- Historial de disparos
- Asistente IA para interpretación

## Tecnologías

- **Backend**: Django 4.2
- **Base de Datos**: SQL Server (mssql-django)
- **Análisis de Datos**: pandas, pandas-ta
- **IA**: LangChain + GPT-4.1-mini
- **Frontend**: Django Templates + Bootstrap 5

## Desarrollo

### Formateo de código
```bash
make format
```

### Ejecutar tests
```bash
make test
```

### Ejecutar linting
```bash
make lint
```

### Docker
```bash
make docker-build
make docker-run
```

## Licencia

MIT