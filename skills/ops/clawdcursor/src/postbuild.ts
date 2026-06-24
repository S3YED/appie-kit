/**
 * Post-build script — runs after tsc.
 * 1. Prints available commands
 * 2. Auto-registers as OpenClaw skill if OpenClaw is installed
 */

import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

// Print available commands
console.log(`
🐾 Clawd Cursor installed! Available commands:

  clawdcursor install   Set up API key, configure pipeline, register as OpenClaw skill
  clawdcursor doctor    Auto-detect and configure your AI
  clawdcursor start     Start the agent
  clawdcursor task      Send a task
  clawdcursor stop      Stop the agent
  clawdcursor dashboard Open the web dashboard
  clawdcursor uninstall Remove all config, data, and OpenClaw registration
`);

// Auto-register as OpenClaw skill
const homeDir = os.homedir();
const skillsDir = path.join(homeDir, '.openclaw', 'skills');
const skillTarget = path.join(skillsDir, 'clawdcursor');
const clawdRoot = path.resolve(__dirname, '..');

if (fs.existsSync(skillsDir)) {
  if (fs.existsSync(skillTarget)) {
    console.log('🔗 OpenClaw skill: already registered');
  } else {
    try {
      fs.symlinkSync(clawdRoot, skillTarget, process.platform === 'win32' ? 'junction' : 'dir');
      console.log(`🔗 OpenClaw skill: registered → ${skillTarget}`);
    } catch {
      // Symlink failed — copy SKILL.md
      try {
        fs.mkdirSync(skillTarget, { recursive: true });
        fs.copyFileSync(
          path.join(clawdRoot, 'SKILL.md'),
          path.join(skillTarget, 'SKILL.md')
        );
        console.log('🔗 OpenClaw skill: registered (copied SKILL.md)');
      } catch {
        console.log('🔗 OpenClaw skill: failed to register (run clawdcursor install to retry)');
      }
    }
  }
} else {
  console.log('🔗 OpenClaw not detected — install OpenClaw (https://openclaw.ai) to use as an AI skill');
}

// Auto-register as Codex skill (Codex UI / Codex agent)
const codexSkillsDir = path.join(homeDir, '.codex', 'skills');
const codexTarget = path.join(codexSkillsDir, 'clawd-cursor');
if (fs.existsSync(codexSkillsDir)) {
  if (fs.existsSync(codexTarget)) {
    console.log('🔗 Codex skill: already registered');
  } else {
    try {
      fs.symlinkSync(clawdRoot, codexTarget, process.platform === 'win32' ? 'junction' : 'dir');
      console.log(`🔗 Codex skill: registered → ${codexTarget}`);
    } catch {
      try {
        fs.mkdirSync(codexTarget, { recursive: true });
        fs.copyFileSync(
          path.join(clawdRoot, 'SKILL.md'),
          path.join(codexTarget, 'SKILL.md')
        );
        console.log('🔗 Codex skill: registered (copied SKILL.md)');
      } catch {
        console.log('🔗 Codex skill: failed to register — symlink/copy ~/.codex/skills/clawd-cursor manually');
      }
    }
  }
}
