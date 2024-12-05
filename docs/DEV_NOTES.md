# Notatki z rozwoju projektu

## [2024-01-08] Konfiguracja projektu
- Utworzono podstawową strukturę projektu
- Skonfigurowano Vue 3 z użyciem create-vue
- Zainstalowano niezbędne zależności
- Skonfigurowano środowisko deweloperskie

### Decyzje techniczne
- Frontend: Vue 3 + Vite
- State Management: Pinia
- Router: Vue Router
- Linter: ESLint + Prettier

### Struktura projektu
time-and-attendance/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── backend/
└── docs/
    ├── API_DOCS.md
    ├── CHANGELOG.md
    ├── DEV_NOTES.md
    └── TODO.md

### Napotkane problemy i rozwiązania
- Rozwiązano problem z podwójnym katalogiem frontend poprzez przeniesienie plików
- Ostrzeżenia npm dotyczące peer dependencies nie wpływają na działanie aplikacji 