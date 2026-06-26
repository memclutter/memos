# Vue.js / frontend standards

- Vue 3 with `<script setup>` and the Composition API. TypeScript by default.
- Build with Vite. Package manager: `pnpm` (preferred) or `npm`, pinned.
- Lint/format with ESLint + Prettier.
- State management with Pinia when shared state is needed.
- Components: `PascalCase` filenames, one component per file.
- Tests with Vitest; component tests with Vue Test Utils.
- Keep API access in a typed client layer, not scattered in components.
