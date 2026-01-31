/**
 * CommandPanel - UI component for displaying and controlling user commands.
 *
 * This panel renders UI components for each command registered with the
 * CommandManager. It supports:
 * - Slider controls for continuous values (e.g., velocity commands)
 * - Button controls for actions (e.g., Reset)
 */

import React, { useCallback, useEffect, useState } from 'react';
import { Box, Button, Collapse, Divider, Paper, ScrollArea, Slider, Text } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconRefresh, IconPlayerPlay } from '@tabler/icons-react';
import {
  getCommandManager,
  type CommandDefinition,
  type SliderCommandConfig,
} from '../core/command';

interface CommandPanelProps {
  /** Callback when reset button is pressed */
  onReset?: () => void;
  /** Whether the panel is enabled */
  enabled?: boolean;
}

/**
 * SliderControl - Renders a slider for a slider command
 */
function SliderControl({
  command,
  value,
  onChange,
  disabled,
}: {
  command: CommandDefinition;
  value: number;
  onChange: (id: string, value: number) => void;
  disabled?: boolean;
}) {
  const config = command.config as SliderCommandConfig;

  return (
    <Box mb="xs">
      <Box
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '0.25rem',
        }}
      >
        <Text size="xs" c="dimmed">
          {config.label}
        </Text>
        <Text size="xs" fw={500} style={{ minWidth: '3em', textAlign: 'right' }}>
          {value.toFixed(2)}
        </Text>
      </Box>
      <Slider
        value={value}
        onChange={(val) => onChange(command.id, val)}
        min={config.min}
        max={config.max}
        step={config.step}
        size="xs"
        disabled={disabled}
        styles={{
          root: { padding: '0 0.25rem' },
          track: { height: 4 },
          thumb: { width: 12, height: 12 },
        }}
      />
    </Box>
  );
}

/**
 * CommandPanel - Main panel component
 */
function CommandPanel({ onReset, enabled = true }: CommandPanelProps) {
  const [commands, setCommands] = useState<CommandDefinition[]>([]);
  const [values, setValues] = useState<Record<string, number>>({});
  const [expanded, { toggle: toggleExpanded }] = useDisclosure(true);

  // Initialize commands from CommandManager
  useEffect(() => {
    const commandManager = getCommandManager();
    const allCommands = commandManager.getCommands();
    setCommands(allCommands);
    setValues(commandManager.getValues());

    // Subscribe to command changes
    const listener = () => {
      setCommands(commandManager.getCommands());
      setValues(commandManager.getValues());
    };
    commandManager.addEventListener(listener);

    return () => {
      commandManager.removeEventListener(listener);
    };
  }, []);

  // Handle slider value changes
  const handleSliderChange = useCallback((id: string, value: number) => {
    const commandManager = getCommandManager();
    commandManager.setValue(id, value);
    setValues((prev) => ({ ...prev, [id]: value }));
  }, []);

  // Handle reset button click
  const handleReset = useCallback(() => {
    const commandManager = getCommandManager();
    commandManager.triggerButton('reset');
    if (onReset) {
      onReset();
    }
  }, [onReset]);

  // Get slider commands (excluding reset button)
  const sliderCommands = commands.filter((cmd) => cmd.config.type === 'slider');

  // Only show panel if we have commands
  if (commands.length === 0) {
    return null;
  }

  return (
    <Paper
      radius="xs"
      shadow="0.1em 0 1em 0 rgba(0,0,0,0.1)"
      style={{
        boxSizing: 'border-box',
        width: '16em',
        overflow: 'hidden',
      }}
    >
      {/* Header */}
      <Box
        style={{
          borderRadius: '0.2em 0.2em 0 0',
          lineHeight: '1.5em',
          cursor: 'pointer',
          position: 'relative',
          fontWeight: 400,
          userSelect: 'none',
          display: 'flex',
          alignItems: 'center',
          padding: '0 0.75em',
          height: '2.75em',
        }}
        onClick={toggleExpanded}
      >
        <div style={{ width: '1.1em' }} />
        <IconPlayerPlay
          color="#40c057"
          style={{
            position: 'absolute',
            width: '1.25em',
            height: '1.25em',
          }}
        />
        <Box
          px="xs"
          style={{
            flexGrow: 1,
            letterSpacing: '-0.5px',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5em',
          }}
          pt="0.1em"
        >
          <span style={{ flexGrow: 1 }}>Commands</span>
        </Box>
      </Box>

      {/* Contents */}
      <Collapse in={expanded}>
        <Divider mx="xs" />
        <ScrollArea.Autosize mah={400}>
          <Box px="sm" py="xs">
            {/* Reset Button */}
            <Button
              variant="light"
              color="red"
              size="xs"
              fullWidth
              leftSection={<IconRefresh size={14} />}
              onClick={handleReset}
              disabled={!enabled}
              mb="sm"
            >
              Reset Simulation
            </Button>

            {/* Divider if there are slider commands */}
            {sliderCommands.length > 0 && <Divider mb="sm" />}

            {/* Slider Commands */}
            {sliderCommands.map((command) => (
              <SliderControl
                key={command.id}
                command={command}
                value={values[command.id] ?? 0}
                onChange={handleSliderChange}
                disabled={!enabled}
              />
            ))}
          </Box>
        </ScrollArea.Autosize>
      </Collapse>
    </Paper>
  );
}

export default CommandPanel;
