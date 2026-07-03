# WAI-Inspired Component Sizing Standards

Based on successful WhatsApp Intelligence (WAI) dashboard architecture patterns.

## File Size Targets

| Component Type | Target Size | WAI Example |
|----------------|-------------|-------------|
| Dashboard/Shell | ≤400 lines | Dashboard.tsx (377 lines) |
| Complex Features | ≤300 lines | AnalyticsView.tsx (299 lines) |
| Simple Components | ≤200 lines | ChatView.tsx (209 lines) |
| Utility/Settings | ≤100 lines | SettingsView.tsx (80 lines) |

## Architecture Patterns

### 1. Component Splitting
- React components should be single-responsibility focused
- Extract shared UI elements into reusable components  
- Keep interface files focused on presentation only

### 2. Logic Extraction
- Extract business logic to custom hooks (`useConversationFilters`, `useMobileOptimizations`)
- Move data fetching/processing to dedicated hooks
- Keep components focused on rendering and user interaction

### 3. Repository Pattern
- Database operations belong in `lib/repositories/` directory
- Centralize Supabase queries and data manipulation
- Examples: `conversationRepository.ts`, `userRepository.ts`

### 4. Code Splitting
- Use `React.lazy()` for dynamic imports of large components
- Implement lazy loading via wrappers like `LazyAnalyticsLoader`
- Reduces initial bundle size and improves performance

## Refactor Indicators

Refactor immediately when:
- Any component approaches 500+ lines
- Adding new features becomes increasingly complex
- Testing individual components becomes difficult
- Multiple unrelated concerns coexist in one file

## Benefits

- **Maintainability**: Smaller files are easier to understand and modify
- **Testability**: Focused components enable better unit testing
- **Reusability**: Extracted hooks and components can be shared
- **Performance**: Code splitting reduces initial load time
- **Collaboration**: Clear boundaries between components aid team work