---
name: react-component-refactoring
description: "Safely refactor large React components into smaller, maintainable pieces using proven patterns"
version: 1.0.0
author: Hermes Agent (refactoring CZA/WAI patterns)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [react, refactor, components, typescript, frontend, modular, safe-refactoring]
    related_skills: [simplify-code, test-driven-development, writing-plans]
---

# React Component Refactoring — Safe Large Component Splitting

Refactor large React components (>500 lines) into smaller, maintainable pieces without breaking functionality. This skill captures patterns observed between CZA (3331 lines across 4 components) and WAI (965 lines) implementations.

## When to Use

Use this skill when:
- A React component exceeds 400-500 lines
- Component contains multiple distinct UI sections or logical concerns
- Code becomes difficult to test or maintain
- You need to follow WAI-style modular architecture

## Refactoring Patterns

### 1. UI Component Isolation (Highest Priority)

Extract reusable UI components from the main component:

```typescript
// BEFORE: Inline components in main file
const NavIcon: React.FC<NavIconProps> = ({ active, icon: Icon, onClick, label }) => (
  <button onClick={onClick} className={`...`}>
    <Icon className="h-5 w-5" />
    <span className="...">{label}</span>
  </button>
);

// AFTER: Separate component file
export interface NavIconProps {
  active: boolean;
  icon: LucideIcon;
  onClick: () => void;
  label: string;
  accentColor?: string;
}

export const NavIcon: React.FC<NavIconProps> = ({ active, icon: Icon, onClick, label, accentColor }) => (
  <button onClick={onClick} className={`...`}>
    <Icon className="h-5 w-5" />
    <span className="...">{label}</span>
  </button>
);
```

**Safety Check:** Verify all props are properly exported and imported

### 2. Hook Extraction (Logic Separation)

Move complex logic and state management into custom hooks:

```typescript
// BEFORE: Logic inline in component
const [conversations, setConversations] = useState<Conversation[]>([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  fetchConversations();
}, []);

// AFTER: Custom hook
const useConversations = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchConversations();
  }, []);

  return { conversations, loading };
};
```

### 3. Repository Pattern (WAI Style)

Extract data access logic into repository files:

```typescript
// lib/repositories/conversationRepository.ts
export const conversationRepository = {
  fetchAll: async (): Promise<Conversation[]> => {
    // Supabase/API calls here
  },
  updateStatus: async (conversationId: string, status: string) => {
    // Update logic
  }
};
```

### 4. Lazy Loading Pattern

Use React.lazy() for code splitting:

```typescript
const LazyAnalytics = lazy(() => import('./AnalyticsView'));
const LazyChatView = lazy(() => import('./ChatView'));
```

## Safety Protocol

### Pre-Refactor Checklist
1. ✅ Run existing tests: `npm test`
2. ✅ Build verification: `npm run build`
3. ✅ Create backup: `git commit -am "pre-refactor backup"`
4. ✅ Verify live site functionality

### Post-Refactor Verification
1. ✅ TypeScript compilation: `npx tsc --noEmit`
2. ✅ Build success: `npm run build`
3. ✅ Tests pass: `npm test`
4. ✅ Live deploy check (Netlify/Vercel)
5. ✅ Manual smoke test critical flows

### Risk Mitigation
- **Never** refactor without tests
- **Always** verify build before pushing
- **Preserve** all existing props and interfaces
- **Maintain** backward compatibility
- **Test** each extracted component individually

## WAI vs CZA Comparison Patterns

| Pattern | WAI Implementation | CZA Implementation |
|---------|-------------------|-------------------|
| Component Size | ~200-400 lines | ~500-1200 lines |
| Hook Usage | Extensive custom hooks | Mixed inline logic |
| Repository Pattern | ✅ Used extensively | ❌ Minimal usage |
| Lazy Loading | ✅ Standard practice | ✅ Implemented |
| File Organization | 19+ focused components | 4 monolithic components |

## Common Pitfalls & Fixes

### Pitfall: Missing Default Export
```typescript
// ❌ Missing export
export default Dashboard;
```

### Pitfall: Prop Interface Mismatch
```typescript
// ✅ Ensure all optional props are marked with ?
export interface NavIconProps {
  active: boolean;
  icon: LucideIcon;
  onClick: () => void;
  label: string;
  accentColor?: string;  // Optional prop
}
```

### Pitfall: CSS Class Consistency
```typescript
// ✅ Preserve all existing class names exactly
className="flex flex-col items-center justify-center gap-1 min-w-[64px] py-2 px-3 rounded-xl transition-all active:scale-95 select-none touch-manipulation"
```

## Implementation Workflow

1. **Analyze**: Identify logical component boundaries
2. **Extract UI**: Move reusable components to separate files
3. **Create Hooks**: Extract complex logic into custom hooks
4. **Add Repositories**: Move data access to repository files
5. **Verify**: Run full test/build/deploy cycle
6. **Commit**: Small, focused commits for each extraction

Adopted from successful WAI patterns: Dashboard.tsx (377 lines), ChatView.tsx (209 lines), AnalyticsView.tsx (299 lines), SettingsView.tsx (80 lines).