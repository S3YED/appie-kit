/**
 * Accessibility Reasoner — Layer 2 in the pipeline.
 *
 * Takes the accessibility tree (text) + a subtask description,
 * sends it to a cheap/fast text-only LLM, and gets back a
 * structured action. No screenshots, no vision model.
 *
 * This handles most desktop app interactions:
 * - Click buttons by name
 * - Fill text fields
 * - Navigate menus
 * - Select list/tree items
 * - Read element values
 *
 * Falls through to Layer 3 (screenshot) when:
 * - No matching element in the accessibility tree
 * - Task requires visual understanding (layout, colors, images)
 * - LLM returns "unsure" or invalid response
 */

import { AccessibilityBridge } from './accessibility';
import type { PipelineConfig } from './providers';
import type { InputAction, A11yAction } from './types';

const SYSTEM_PROMPT = `You analyze accessibility trees to execute desktop tasks. Given a task and the current UI state (windows + elements), return ONE JSON action.

ACTIONS:
{"action":"a11y_click","name":"Button Name","controlType":"Button","description":"..."}
{"action":"a11y_set_value","name":"Field Name","controlType":"Edit","value":"text","description":"..."}
{"action":"a11y_focus","name":"Element","controlType":"Edit","description":"..."}
{"action":"key_press","key":"Return|Tab|Escape|ctrl+s|...","description":"..."}
{"action":"type","text":"hello","description":"..."}
{"action":"done","description":"Task already completed based on UI state"}
{"action":"unsure","description":"Cannot determine action from accessibility tree alone"}

RULES:
1. Match elements by name (case-insensitive, partial match OK)
2. Prefer a11y_click over coordinate clicks — more reliable
3. If the target element isn't in the tree, return {"action":"unsure"}
4. For typing into fields: a11y_focus first, then type
5. Return ONLY valid JSON, no other text
6. PREFER keyboard shortcuts — faster and more reliable than clicking:
   - Save: key_press "ctrl+s" instead of clicking Save button
   - Close: key_press "alt+F4" instead of clicking X
   - New tab: key_press "ctrl+t" | Address bar: key_press "ctrl+l"
   - Calculator: type "1337*42=" instead of clicking individual buttons
   - Select all: "ctrl+a" | Copy: "ctrl+c" | Paste: "ctrl+v"
   - If app is already open, focus it instead of re-launching
7. VERIFY outcomes — check the UI state after actions to confirm success`;

interface ReasonerResult {
  handled: boolean;
  action?: InputAction;
  description: string;
  /** true if the reasoner says "I can't handle this" → fall through to Layer 3 */
  unsure?: boolean;
}

export class A11yReasoner {
  private a11y: AccessibilityBridge;
  private pipelineConfig: PipelineConfig;
  private consecutiveFailures = 0;
  private readonly MAX_FAILURES = 3;
  private disabled = false;

  constructor(a11y: AccessibilityBridge, pipelineConfig: PipelineConfig) {
    this.a11y = a11y;
    this.pipelineConfig = pipelineConfig;
  }

  /** Check if reasoner is available and not circuit-broken */
  isAvailable(): boolean {
    return this.pipelineConfig.layer2.enabled && !this.disabled;
  }

  /**
   * Try to handle a subtask using only the accessibility tree.
   * Returns { handled: false } if it can't → caller should use Layer 3.
   */
  async reason(subtask: string): Promise<ReasonerResult> {
    if (!this.isAvailable()) {
      return { handled: false, description: 'Layer 2 disabled' };
    }

    try {
      // Get accessibility context
      const activeWindow = await this.a11y.getActiveWindow();
      const context = await this.a11y.getScreenContext(activeWindow?.processId);

      if (!context || context.includes('unavailable')) {
        return { handled: false, description: 'Accessibility tree unavailable' };
      }

      // Build prompt
      const userMessage = `TASK: ${subtask}\n\nCURRENT UI STATE:\n${context}`;

      // Call cheap text model
      const start = performance.now();
      const response = await this.callTextModel(userMessage);
      const latency = Math.round(performance.now() - start);

      console.log(`   🧠 Layer 2 (${this.pipelineConfig.layer2.model}): ${latency}ms`);

      // Parse response
      const result = this.parseResponse(response);

      if (result.unsure) {
        console.log(`   🤷 Layer 2 unsure: ${result.description} → falling through to Layer 3`);
        return { handled: false, description: result.description, unsure: true };
      }

      if (result.handled) {
        this.consecutiveFailures = 0; // Reset circuit breaker
        console.log(`   ✅ Layer 2 handled: ${result.description}`);
      }

      return result;
    } catch (err) {
      this.consecutiveFailures++;
      console.log(`   ⚠️ Layer 2 error (${this.consecutiveFailures}/${this.MAX_FAILURES}): ${err}`);

      // Circuit breaker
      if (this.consecutiveFailures >= this.MAX_FAILURES) {
        this.disabled = true;
        console.log(`   🔴 Layer 2 circuit breaker tripped — disabled for this session`);
      }

      return { handled: false, description: `Layer 2 error: ${err}` };
    }
  }

  /** Reset circuit breaker (e.g., after doctor re-diagnoses) */
  reset(): void {
    this.disabled = false;
    this.consecutiveFailures = 0;
  }

  private parseResponse(response: string): ReasonerResult {
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (!jsonMatch) {
        return { handled: false, description: 'No JSON in response', unsure: true };
      }

      const parsed = JSON.parse(jsonMatch[0]);

      if (parsed.action === 'unsure') {
        return { handled: false, description: parsed.description || 'Unsure', unsure: true };
      }

      if (parsed.action === 'done') {
        return { handled: true, description: parsed.description || 'Already done' };
      }

      // Map to InputAction
      const action = this.mapAction(parsed);
      if (!action) {
        return { handled: false, description: 'Could not map action', unsure: true };
      }

      return {
        handled: true,
        action,
        description: parsed.description || parsed.action,
      };
    } catch {
      return { handled: false, description: 'Failed to parse response', unsure: true };
    }
  }

  private mapAction(parsed: any): InputAction | null {
    switch (parsed.action) {
      case 'a11y_click':
        return {
          kind: 'a11y_click',
          name: parsed.name,
          controlType: parsed.controlType,
        } as A11yAction;

      case 'a11y_set_value':
        return {
          kind: 'a11y_set_value',
          name: parsed.name,
          controlType: parsed.controlType,
          value: parsed.value,
        } as A11yAction;

      case 'a11y_focus':
        return {
          kind: 'a11y_focus',
          name: parsed.name,
          controlType: parsed.controlType,
        } as A11yAction;

      case 'key_press':
        return { kind: 'key_press', key: parsed.key } as InputAction;

      case 'type':
        return { kind: 'type', text: parsed.text } as InputAction;

      default:
        return null;
    }
  }

  private async callTextModel(userMessage: string): Promise<string> {
    const { model, baseUrl } = this.pipelineConfig.layer2;
    const apiKey = this.pipelineConfig.apiKey;
    const provider = this.pipelineConfig.provider;

    if (provider.openaiCompat || baseUrl.includes('localhost') || baseUrl.includes('11434')) {
      // OpenAI-compatible (Ollama, OpenAI, Kimi)
      const response = await fetch(`${baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...provider.authHeader(apiKey),
        },
        body: JSON.stringify({
          model,
          max_tokens: 200,
          temperature: 0,
          messages: [
            { role: 'system', content: SYSTEM_PROMPT },
            { role: 'user', content: userMessage },
          ],
        }),
        signal: AbortSignal.timeout(10000),
      });

      const data = await response.json() as any;
      if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
      return data.choices?.[0]?.message?.content || '';
    } else {
      // Anthropic
      const response = await fetch(`${baseUrl}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...provider.authHeader(apiKey),
        },
        body: JSON.stringify({
          model,
          max_tokens: 200,
          system: SYSTEM_PROMPT,
          messages: [{ role: 'user', content: userMessage }],
        }),
        signal: AbortSignal.timeout(10000),
      });

      const data = await response.json() as any;
      if (data.error) throw new Error(data.error.message || JSON.stringify(data.error));
      return data.content?.[0]?.text || '';
    }
  }
}
