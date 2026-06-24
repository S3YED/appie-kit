import { describe, expect, it } from 'vitest';
import { findShortcut, resolveShortcutKey, SHORTCUTS } from '../src/shortcuts';

describe('shortcuts registry', () => {
  it('matches common natural language intents', () => {
    expect(findShortcut('scroll down', 'linux')?.combo).toBe('PageDown');
    expect(findShortcut('new tab', 'linux')?.combo).toBe('Control+t');
    expect(findShortcut('reddit upvote', 'linux')?.combo).toBe('a');
  });

  it('supports press-prefixed intents', () => {
    const match = findShortcut('press refresh', 'win32');
    expect(match?.combo).toBe('F5');
    expect(match?.canonicalIntent).toBe('refresh');
    expect(match?.matchType).toBe('exact');
  });

  it('uses platform-specific variants', () => {
    const refresh = SHORTCUTS.find(s => s.id === 'refresh');
    expect(refresh).toBeTruthy();
    expect(resolveShortcutKey(refresh!, 'darwin')).toBe('Super+r');
    expect(resolveShortcutKey(refresh!, 'linux')).toBe('F5');
  });

  it('supports fuzzy matching for minor typos', () => {
    const fuzzyRefresh = findShortcut('refesh', 'linux');
    expect(fuzzyRefresh?.combo).toBe('F5');
    expect(fuzzyRefresh?.matchType).toBe('fuzzy');

    const fuzzyNewTab = findShortcut('newtab', 'linux');
    expect(fuzzyNewTab?.combo).toBe('Control+t');
  });

  it('applies context-aware constraints for social shortcuts', () => {
    expect(findShortcut('upvote', 'linux')).toBeNull();

    const socialFromContext = findShortcut('upvote', 'linux', { contextHint: 'reddit.com frontpage' });
    expect(socialFromContext?.combo).toBe('a');

    const socialFromTask = findShortcut('reddit upvote', 'linux');
    expect(socialFromTask?.combo).toBe('a');
  });

  it('returns null for unknown intents', () => {
    expect(findShortcut('dance now')).toBeNull();
  });
});
