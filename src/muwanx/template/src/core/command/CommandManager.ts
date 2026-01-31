/**
 * CommandManager - Manages user commands that can be sent to the policy.
 *
 * Commands are user inputs (like velocity targets) that get passed to the
 * ONNX policy as part of the observation. The CommandManager:
 * - Defines available commands with their types and ranges
 * - Stores current command values
 * - Provides an interface for UI components to update values
 * - Provides observation values for the policy
 */

export type CommandType = 'slider' | 'button';

export interface SliderCommandConfig {
  type: 'slider';
  name: string;
  label: string;
  min: number;
  max: number;
  step: number;
  defaultValue: number;
}

export interface ButtonCommandConfig {
  type: 'button';
  name: string;
  label: string;
}

export type CommandConfig = SliderCommandConfig | ButtonCommandConfig;

export interface CommandDefinition {
  id: string;
  config: CommandConfig;
}

export type CommandEventType = 'change' | 'reset' | 'button';

export interface CommandEvent {
  type: CommandEventType;
  commandId: string;
  value?: number;
}

export type CommandEventListener = (event: CommandEvent) => void;

/**
 * Default velocity command configuration
 */
export const DEFAULT_VELOCITY_COMMANDS: CommandConfig[] = [
  {
    type: 'slider',
    name: 'vel_x',
    label: 'Forward Velocity',
    min: -1.0,
    max: 1.0,
    step: 0.05,
    defaultValue: 0.5,
  },
  {
    type: 'slider',
    name: 'vel_y',
    label: 'Lateral Velocity',
    min: -0.5,
    max: 0.5,
    step: 0.05,
    defaultValue: 0.0,
  },
  {
    type: 'slider',
    name: 'yaw_rate',
    label: 'Yaw Rate',
    min: -1.0,
    max: 1.0,
    step: 0.05,
    defaultValue: 0.0,
  },
];

export class CommandManager {
  private commands: Map<string, CommandDefinition> = new Map();
  private values: Map<string, number> = new Map();
  private listeners: Set<CommandEventListener> = new Set();
  private resetCallback: (() => void) | null = null;

  constructor() {
    // Reset command is always available by default
    this.registerCommand({
      type: 'button',
      name: 'reset',
      label: 'Reset',
    });
  }

  /**
   * Register a command with the manager
   */
  registerCommand(config: CommandConfig): void {
    const id = config.name;
    this.commands.set(id, { id, config });

    // Initialize slider values to default
    if (config.type === 'slider') {
      this.values.set(id, config.defaultValue);
    }
  }

  /**
   * Register multiple commands at once
   */
  registerCommands(configs: CommandConfig[]): void {
    for (const config of configs) {
      this.registerCommand(config);
    }
  }

  /**
   * Get all registered commands
   */
  getCommands(): CommandDefinition[] {
    return Array.from(this.commands.values());
  }

  /**
   * Get a specific command by ID
   */
  getCommand(id: string): CommandDefinition | undefined {
    return this.commands.get(id);
  }

  /**
   * Get the current value of a slider command
   */
  getValue(id: string): number {
    return this.values.get(id) ?? 0;
  }

  /**
   * Get all current slider values
   */
  getValues(): Record<string, number> {
    const result: Record<string, number> = {};
    for (const [id, value] of this.values) {
      result[id] = value;
    }
    return result;
  }

  /**
   * Get velocity command values as an array [vel_x, vel_y, yaw_rate]
   */
  getVelocityCommand(): Float32Array {
    const velX = this.values.get('vel_x') ?? 0.5;
    const velY = this.values.get('vel_y') ?? 0.0;
    const yawRate = this.values.get('yaw_rate') ?? 0.0;
    return new Float32Array([velX, velY, yawRate]);
  }

  /**
   * Set the value of a slider command
   */
  setValue(id: string, value: number): void {
    const command = this.commands.get(id);
    if (!command || command.config.type !== 'slider') {
      return;
    }

    const config = command.config as SliderCommandConfig;
    const clampedValue = Math.max(config.min, Math.min(config.max, value));
    this.values.set(id, clampedValue);

    this.emit({
      type: 'change',
      commandId: id,
      value: clampedValue,
    });
  }

  /**
   * Trigger a button command
   */
  triggerButton(id: string): void {
    const command = this.commands.get(id);
    if (!command || command.config.type !== 'button') {
      return;
    }

    if (id === 'reset' && this.resetCallback) {
      this.resetCallback();
    }

    this.emit({
      type: 'button',
      commandId: id,
    });
  }

  /**
   * Reset all slider values to their defaults
   */
  resetToDefaults(): void {
    for (const [id, command] of this.commands) {
      if (command.config.type === 'slider') {
        const config = command.config as SliderCommandConfig;
        this.values.set(id, config.defaultValue);
      }
    }

    this.emit({
      type: 'reset',
      commandId: '*',
    });
  }

  /**
   * Set the reset callback (called when reset button is pressed)
   */
  setResetCallback(callback: () => void): void {
    this.resetCallback = callback;
  }

  /**
   * Add an event listener
   */
  addEventListener(listener: CommandEventListener): void {
    this.listeners.add(listener);
  }

  /**
   * Remove an event listener
   */
  removeEventListener(listener: CommandEventListener): void {
    this.listeners.delete(listener);
  }

  /**
   * Emit an event to all listeners
   */
  private emit(event: CommandEvent): void {
    for (const listener of this.listeners) {
      try {
        listener(event);
      } catch (error) {
        console.warn('[CommandManager] Listener error:', error);
      }
    }
  }

  /**
   * Clear all commands (except reset)
   */
  clear(): void {
    const resetCommand = this.commands.get('reset');
    this.commands.clear();
    this.values.clear();
    if (resetCommand) {
      this.commands.set('reset', resetCommand);
    }
  }

  /**
   * Dispose of the command manager
   */
  dispose(): void {
    this.commands.clear();
    this.values.clear();
    this.listeners.clear();
    this.resetCallback = null;
  }
}

// Singleton instance for global access
let globalCommandManager: CommandManager | null = null;

export function getCommandManager(): CommandManager {
  if (!globalCommandManager) {
    globalCommandManager = new CommandManager();
  }
  return globalCommandManager;
}

export function resetCommandManager(): void {
  if (globalCommandManager) {
    globalCommandManager.dispose();
    globalCommandManager = null;
  }
}
