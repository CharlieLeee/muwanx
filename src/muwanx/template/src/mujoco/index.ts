// Re-export types from mujoco_wasm.d.ts
export type {
  MainModule,
  MjModel,
  MjData,
  MjVFS,
  ClassHandle,
} from './mujoco_wasm';

import type { MainModule } from './mujoco_wasm';

// Dynamic loader that imports from public folder at runtime
const loadMujoco = async (): Promise<MainModule> => {
  const baseUrl = import.meta.env.BASE_URL || '/';
  const modulePath = `${baseUrl}assets/mujoco_wasm.js`.replace(/\/+/g, '/');
  const module = await import(/* @vite-ignore */ modulePath);
  return module.default();
};

export default loadMujoco;
