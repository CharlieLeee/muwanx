# MuJoCo WASM 3.3.7 Migration Guide

## Summary of Changes

This document provides a comprehensive guide for migrating from MuJoCo WASM 2.3.1 to 3.3.7. The migration was successfully completed for the muwanx project, and this guide documents all the changes, common pitfalls, and solutions encountered during the process.

## Overview

The MuJoCo WASM 3.3.7 API represents a significant departure from version 2.3.1, with changes that align more closely with the native MuJoCo C++ API. Key changes include:

- Unified data structure (`MjData` replaces `State` and `Simulation`)
- Direct property access (no function calls with parentheses)
- Global functions for simulation stepping
- Different memory management patterns
- Updated naming conventions (camelCase for static methods)

## Core API Changes

### 1. Model and Data Objects

**Old API (2.3.1):**
```javascript
model = mujoco.Model.load_from_xml('/working/model.xml');
state = new mujoco.State(model);
simulation = new mujoco.Simulation(model, state);
```

**New API (3.3.7):**
```javascript
mjModel = mujoco.MjModel.loadFromXML('/working/model.xml');
mjData = new mujoco.MjData(mjModel);
```

### 2. Model Properties Access

**CRITICAL:** In the new API, ALL properties use direct access (NO parentheses):

This is the most common source of errors during migration. The old API used function-style getters like `model.ngeom()`, but the new API uses direct property access like `model.ngeom`.

**Scalar properties:**
   - `model.ngeom`, `model.nbody`, `model.nlight`, `model.njnt`, `model.nu`, `model.ntendon`
   - `model.names` (buffer access)
   - `model.opt` (options object - direct access, not `getOptions()`)
   - `model.opt.timestep` (timestep within opt)

**Array/buffer properties (also direct access):**
   - `model.geom_type`, `model.geom_bodyid`, `model.geom_size`, `model.geom_group`
   - `model.mesh_vert`, `model.mesh_normal`, `model.mesh_face`
   - `model.geom_rgba`, `model.mat_rgba`, `model.tex_rgb`
   - All other array-like properties

**Migration Examples:**
```javascript
// WRONG (Old API style - will throw "is not a function" errors)
for (let g = 0; g < model.ngeom(); g++) { }  // ❌ TypeError
const names = new Uint8Array(model.names());  // ❌ TypeError
const timestep = model.getOptions().timestep; // ❌ TypeError
const type = model.geom_type()[i];            // ❌ TypeError

// CORRECT (New API - direct property access)
for (let g = 0; g < model.ngeom; g++) { }     // ✅
const names = new Uint8Array(model.names);    // ✅
const timestep = model.opt.timestep;          // ✅
const type = model.geom_type[i];              // ✅
const bodyId = model.geom_bodyid[g];          // ✅
const vertices = model.mesh_vert;             // ✅
```

### 3. Simulation Functions

**Old API:**
```javascript
simulation.step();
simulation.forward();
simulation.resetData();
simulation.applyForce(fx, fy, fz, tx, ty, tz, px, py, pz, bodyId);
```

**New API:**
```javascript
mujoco.mj_step(mjModel, mjData);
mujoco.mj_forward(mjModel, mjData);
mujoco.mj_resetData(mjModel, mjData);

// Apply force/torque - direct approach (recommended)
// Apply directly to xfrc_applied (Cartesian forces)
const offset = bodyId * 6;  // Each body has [fx, fy, fz, tx, ty, tz]

// If applying force at a point (not center of mass), compute torque
const bodyPos = new THREE.Vector3(
    mjData.xpos[bodyId * 3], 
    mjData.xpos[bodyId * 3 + 1], 
    mjData.xpos[bodyId * 3 + 2]
);
const r = new THREE.Vector3(px - bodyPos.x, py - bodyPos.y, pz - bodyPos.z);
const f = new THREE.Vector3(fx, fy, fz);
const torque = new THREE.Vector3().crossVectors(r, f);

// Set forces in xfrc_applied
mjData.xfrc_applied[offset + 0] = fx;
mjData.xfrc_applied[offset + 1] = fy;
mjData.xfrc_applied[offset + 2] = fz;
mjData.xfrc_applied[offset + 3] = torque.x;
mjData.xfrc_applied[offset + 4] = torque.y;
mjData.xfrc_applied[offset + 5] = torque.z;
```

**Note:** 
- All simulation functions are now global functions that take `mjModel` and `mjData` as the first two parameters
- **Recommended approach**: Directly write to `mjData.xfrc_applied` which holds Cartesian forces/torques for each body
- `xfrc_applied` is sized `(nbody × 6)` with format `[force_x, force_y, force_z, torque_x, torque_y, torque_z]` per body
- If applying force at a point (not center of mass), compute the resulting torque using cross product: `τ = r × F`
- This mimics the behavior of the old `simulation.applyForce()` method from MuJoCo WASM 2.3.1

### 4. Data Access

All data fields use direct property access (NO parentheses):

**Old:** `simulation.qpos`, `simulation.qvel`, `simulation.ctrl`  
**New:** `mjData.qpos`, `mjData.qvel`, `mjData.ctrl`

Examples:
- `simulation.xpos` → `mjData.xpos`
- `simulation.xquat` → `mjData.xquat`
- `simulation.light_xpos` → `mjData.light_xpos`
- `simulation.ten_wrapadr[t]` → `mjData.ten_wrapadr[t]`

### 5. Model Options

**Old:** `model.getOptions().timestep`  
**New:** `mjModel.opt.timestep`

The `opt` is a direct property, and `timestep` is a direct property of that object.

### 6. Memory Management

**Old:** `.free()` method  
**New:** `.delete()` method

```javascript
// Old
if (simulation) simulation.free();
if (state) state.free();
if (model) model.free();

// New
if (mjData) mjData.delete();
if (mjModel) mjModel.delete();
```

## Files Updated

All files have been successfully migrated to MuJoCo WASM 3.3.7:

### Core Runtime Files ✅
- ✅ `src/mujoco_wasm/runtime/utils/mujocoScene.js` - Model loading and scene initialization
- ✅ `src/mujoco_wasm/runtime/MujocoRuntime.js` - Main simulation loop and manager coordination
- ✅ `src/mujoco_wasm/examples/onnxHelper.js` - ONNX policy loading with improved error handling

### Manager Files ✅
- ✅ `src/mujoco_wasm/runtime/managers/actions/IsaacActionManager.js` - Action manager using mjData
- ✅ `src/mujoco_wasm/runtime/managers/observations/ConfigObservationManager.js` - Observation manager coordinator
- ✅ `src/mujoco_wasm/runtime/managers/environment/LocomotionEnvManager.js` - Environment manager using mj_applyFT

### Observation Components ✅
- ✅ `src/mujoco_wasm/runtime/observations/atomic.js` - All atomic observation classes:
  - `BaseLinearVelocity`
  - `BaseAngularVelocity`
  - `ProjectedGravity`
  - `JointPositions`
  - `JointVelocities`
  - `PreviousActions`
  - `SimpleVelocityCommand`
- ✅ `src/mujoco_wasm/runtime/observations/commands.js` - Command observation classes:
  - `VelocityCommand`
  - `VelocityCommandWithOscillators`
  - `ImpedanceCommand`
  - `Oscillator`

## Detailed Migration Patterns

### 1. Observation Manager Classes

All observation classes need to be updated to use `mjData` instead of `simulation`:

**Step 1: Update constructor signature and store mjData**
```javascript
// Old
constructor(model, simulation, runtime, kwargs = {}) {
    this.mjModel = model;
    this.simulation = simulation;
    this.runtime = runtime;
}

// New
constructor(model, mjData, runtime, kwargs = {}) {
    this.mjModel = model;
    this.mjData = mjData;
    this.runtime = runtime;
}
```

**Step 2: Update all data access (NO parentheses)**
```javascript
// Old
const quat = this.simulation.qpos.subarray(3, 7);
const vel = this.simulation.qvel.subarray(0, 3);
const ctrl = this.simulation.ctrl;

// New
const quat = this.mjData.qpos.subarray(3, 7);
const vel = this.mjData.qvel.subarray(0, 3);
const ctrl = this.mjData.ctrl;
```

**Complete Example - ProjectedGravity class:**
```javascript
// Before migration
export class ProjectedGravity {
    constructor(model, simulation, runtime, kwargs = {}) {
        this.mjModel = model;
        this.simulation = simulation;
        this.runtime = runtime;
        const { joint_name = "floating_base_joint" } = kwargs;
        this.joint_name = joint_name;
        this.joint_id = mujocoFindId(model, 'joint', joint_name);
    }

    compute() {
        const qpos_adr = this.mjModel.jnt_qposadr[this.joint_id];
        const quat_idx = qpos_adr + 3;
        const quat = this.simulation.qpos.subarray(quat_idx, quat_idx + 4);
        const gravity_world = new THREE.Vector3(0, 0, -1);
        const base_quat = new THREE.Quaternion(quat[1], quat[2], quat[3], quat[0]);
        const gravity_base = gravity_world.applyQuaternion(base_quat.invert());
        return new Float32Array([gravity_base.x, gravity_base.y, gravity_base.z]);
    }
}

// After migration
export class ProjectedGravity {
    constructor(model, mjData, runtime, kwargs = {}) {
        this.mjModel = model;
        this.mjData = mjData;
        this.runtime = runtime;
        const { joint_name = "floating_base_joint" } = kwargs;
        this.joint_name = joint_name;
        this.joint_id = mujocoFindId(model, 'joint', joint_name);
    }

    compute() {
        const qpos_adr = this.mjModel.jnt_qposadr[this.joint_id];
        const quat_idx = qpos_adr + 3;
        const quat = this.mjData.qpos.subarray(quat_idx, quat_idx + 4);
        const gravity_world = new THREE.Vector3(0, 0, -1);
        const base_quat = new THREE.Quaternion(quat[1], quat[2], quat[3], quat[0]);
        const gravity_base = gravity_world.applyQuaternion(base_quat.invert());
        return new Float32Array([gravity_base.x, gravity_base.y, gravity_base.z]);
    }
}
```

### 2. Action Manager Classes

Action managers need updates in their callback methods and data access:

**Step 1: Update callback signatures**
```javascript
// Old
async onSceneLoaded({ model, simulation, assetMeta }) {
    this.mjModel = model;
    this.simulation = simulation;
    this.timestep = model.getOptions().timestep;
}

// New
async onSceneLoaded({ model, mjData, assetMeta }) {
    this.mjModel = model;
    this.mjData = mjData;
    this.timestep = model.opt.timestep;  // Direct property access!
}
```

**Step 2: Update control access**
```javascript
// Old
this.simulation.ctrl[i] = value;
this.simulation.qpos[idx] = position;

// New
this.mjData.ctrl[i] = value;
this.mjData.qpos[idx] = position;
```

**Complete Example - IsaacActionManager:**
```javascript
// Before migration
async onSceneLoaded({ model, simulation, assetMeta }) {
    this.mjModel = model;
    this.simulation = simulation;
    this.timestep = model.getOptions().timestep;
    
    // ... initialization code ...
}

applyAction(action) {
    for (let i = 0; i < this.action_indices.length; i++) {
        const targetPos = this.default_positions[i] + action[i] * this.actionScale;
        const currentPos = this.simulation.qpos[this.qpos_indices[i]];
        const currentVel = this.simulation.qvel[this.qvel_indices[i]];
        this.simulation.ctrl[this.action_indices[i]] = this.pd_control(
            targetPos, currentPos, currentVel
        );
    }
}

// After migration
async onSceneLoaded({ model, mjData, assetMeta }) {
    this.mjModel = model;
    this.mjData = mjData;
    this.timestep = model.opt.timestep;  // Changed from getOptions()
    
    // ... initialization code ...
}

applyAction(action) {
    for (let i = 0; i < this.action_indices.length; i++) {
        const targetPos = this.default_positions[i] + action[i] * this.actionScale;
        const currentPos = this.mjData.qpos[this.qpos_indices[i]];
        const currentVel = this.mjData.qvel[this.qvel_indices[i]];
        this.mjData.ctrl[this.action_indices[i]] = this.pd_control(
            targetPos, currentPos, currentVel
        );
    }
}
```

### 3. Manager Coordinator Updates

The `ConfigObservationManager` and similar coordinator classes need to pass `mjData` to observation instances:

**Update onPolicyLoaded signature:**
```javascript
// Old
async onPolicyLoaded({ config, model, simulation, assetMeta }) {
    this.observationGroups[key] = components.map(obsConfigItem => 
        this.createObservationInstance({
            obsConfig: obsConfigItem,
            model,
            simulation,  // ❌ Wrong parameter
            assetMeta,
        })
    );
}

// New
async onPolicyLoaded({ config, model, mjData, assetMeta }) {
    this.observationGroups[key] = components.map(obsConfigItem => 
        this.createObservationInstance({
            obsConfig: obsConfigItem,
            model,
            mjData,  // ✅ Correct parameter
            assetMeta,
        })
    );
}
```

**Update createObservationInstance:**
```javascript
// Old
createObservationInstance({ obsConfig, model, simulation }) {
    const ObsClass = observationRegistry[obsConfig.name];
    return new ObsClass(model, simulation, this.runtime, kwargs);
}

// New
createObservationInstance({ obsConfig, model, mjData }) {
    const ObsClass = observationRegistry[obsConfig.name];
    return new ObsClass(model, mjData, this.runtime, kwargs);
}
```

### 4. Runtime Step Context

Update the context object passed to manager lifecycle methods:

```javascript
// Old context
const stepContext = {
    model: this.mjModel,
    simulation: this.simulation,
    timestep: this.timestep,
};

// New context
const stepContext = {
    model: this.mjModel,
    mjData: this.mjData,
    timestep: this.timestep,
};
```

### 5. Scene Loading and Initialization

**Complete mujocoScene.js loadSceneFromURL function:**
```javascript
// New API implementation
export async function loadSceneFromURL(mujoco, url) {
    const response = await fetch(url);
    const xml = await response.text();
    
    mujoco.FS.writeFile('/working/scene.xml', xml);
    
    const mjModel = mujoco.MjModel.loadFromXML('/working/scene.xml');
    const mjData = new mujoco.MjData(mjModel);
    
    mujoco.mj_forward(mjModel, mjData);
    
    return { mjModel, mjData };
}
```

**Main runtime initialization:**
```javascript
// In MujocoRuntime.js
async loadEnvironment(sceneURL) {
    const { mjModel, mjData } = await loadSceneFromURL(this.mujoco, sceneURL);
    this.mjModel = mjModel;
    this.mjData = mjData;
    this.timestep = mjModel.opt.timestep;
    
    // Initialize managers with new parameters
    if (this.actionManager) {
        await this.actionManager.onSceneLoaded({
            model: mjModel,
            mjData: mjData,
            assetMeta: this.observationContext?.assetMeta,
        });
    }
}
```

## Key Differences Summary

1. **No more State/Simulation split**: `MjData` combines what was previously `State` and `Simulation`
2. **Direct property access**: ALL model/data properties are accessed directly (NO function calls with `()`)
3. **Global functions**: Step and forward are now global functions that take model and data as parameters
4. **Consistent naming**: `MjModel` and `MjData` follow MuJoCo C++ naming conventions
5. **Memory management**: Use `.delete()` instead of `.free()`
6. **Static method naming**: `loadFromXML` instead of `load_from_xml` (camelCase)

## Testing Checklist

After migration, verify:
- [ ] Model loads without errors
- [ ] Simulation steps correctly
- [ ] Robot visualization updates
- [ ] Policy inference works (if applicable)
- [ ] Reset functionality works
- [ ] Memory cleanup (no leaks on dispose)
- [ ] All managers receive correct parameters
- [ ] Observations are computed correctly
- [ ] Actions are applied correctly

## Common Pitfalls and Solutions

### 1. Property Access Errors (Most Common)

**Error:** `TypeError: model.ngeom is not a function`

**Cause:** Attempting to call a property as a function (old API style)

**Solution:** Remove parentheses - use direct property access
```javascript
// ❌ Wrong
for (let i = 0; i < model.ngeom(); i++) { }

// ✅ Correct
for (let i = 0; i < model.ngeom; i++) { }
```

### 2. Undefined Light Properties

**Error:** `TypeError: Cannot read properties of undefined (reading '0')`

**Cause:** Some models don't define optional light properties like `light_directional` or `light_attenuation`

**Solution:** Always check property existence before accessing:
```javascript
// ❌ Wrong - assumes lights exist
for (let l = 0; l < model.nlight; l++) {
    const directional = model.light_directional[l];  // May crash
}

// ✅ Correct - checks first
if (model.nlight > 0 && model.light_directional) {
    for (let l = 0; l < model.nlight; l++) {
        const directional = model.light_directional[l];
    }
}
```

### 3. Model Options Access

**Error:** `TypeError: model.getOptions is not a function`

**Cause:** Using old API method to access options

**Solution:** Use direct property access
```javascript
// ❌ Wrong
const timestep = model.getOptions().timestep;

// ✅ Correct
const timestep = model.opt.timestep;
```

### 4. Apply Force/Torque Method

**Error:** `TypeError: this.mjData.applyForce is not a function` or `BindingError: function mj_applyFT called with X arguments, expected 7` or `Error: Expected a TypedArray or WasmBuffer` or `Error: qfrc_target must have size X, got Y`

**Cause:** The old `simulation.applyForce()` method has been replaced with a global function that requires specific Float64Array parameters

**Solution:** Use `mj_applyFT()` global function with properly sized Float64Array parameters
```javascript
### 4. Apply Force/Torque Method

**Error:** `TypeError: this.mjData.applyForce is not a function`

**Cause:** The old `simulation.applyForce()` method no longer exists

**Solution:** Apply forces directly to `mjData.xfrc_applied` (recommended approach)
```javascript
// ❌ Wrong (old API)
this.mjData.applyForce(
    force.x, force.y, force.z,
    torque.x, torque.y, torque.z,
    point.x, point.y, point.z,
    bodyId
);

// ✅ Correct (new API - direct Cartesian force application)
const offset = bodyId * 6;  // xfrc_applied format: [fx, fy, fz, tx, ty, tz] per body

// Get body center of mass position
const bodyPos = new THREE.Vector3(
    this.mjData.xpos[bodyId * 3],
    this.mjData.xpos[bodyId * 3 + 1],
    this.mjData.xpos[bodyId * 3 + 2]
);

// Compute torque from force at point: τ = r × F
const r = new THREE.Vector3(point.x - bodyPos.x, point.y - bodyPos.y, point.z - bodyPos.z);
const f = new THREE.Vector3(force.x, force.y, force.z);
const torque = new THREE.Vector3().crossVectors(r, f);

// Apply force and computed torque directly to xfrc_applied
this.mjData.xfrc_applied[offset + 0] = force.x;
this.mjData.xfrc_applied[offset + 1] = force.y;
this.mjData.xfrc_applied[offset + 2] = force.z;
this.mjData.xfrc_applied[offset + 3] = torque.x;
this.mjData.xfrc_applied[offset + 4] = torque.y;
this.mjData.xfrc_applied[offset + 5] = torque.z;
```

**Important Notes:** 
- **Recommended approach**: Directly write to `mjData.xfrc_applied` array
- `xfrc_applied` is sized `(nbody × 6)` where each body has `[force_x, force_y, force_z, torque_x, torque_y, torque_z]`
- When applying force at a specific point (not center of mass), compute the resulting torque using `τ = r × F`
- This approach mimics the old `simulation.applyForce()` behavior and is simpler than using `mj_applyFT`
- **CRITICAL**: You must clear `xfrc_applied` at the beginning of each step if you want forces to only apply when actively set:
  ```javascript
  // Clear forces before each step
  for (let i = 0; i < mjData.xfrc_applied.length; i++) {
      mjData.xfrc_applied[i] = 0.0;
  }
  ```

// ❌ Also wrong (using regular arrays)
this.runtime.mujoco.mj_applyFT(
    this.mjModel, this.mjData,
    [force.x, force.y, force.z],      // ❌ Regular array
    [torque.x, torque.y, torque.z],   // ❌ Regular array
    [point.x, point.y, point.z],      // ❌ Regular array
    bodyId,
    new Float64Array()                 // ❌ Wrong size
);

// ✅ Correct (new API - Float64Array parameters with correct sizes)
const qfrc = new Float64Array(this.mjModel.nv);
this.runtime.mujoco.mj_applyFT(
    this.mjModel,
    this.mjData,
    new Float64Array([force.x, force.y, force.z]),    // ✅ Float64Array
    new Float64Array([torque.x, torque.y, torque.z]), // ✅ Float64Array
    new Float64Array([point.x, point.y, point.z]),    // ✅ Float64Array
    bodyId,
    qfrc  // ✅ qfrc output buffer sized to model.nv
);
// ✅ CRITICAL: Add computed forces to qfrc_applied
for (let i = 0; i < this.mjModel.nv; i++) {
    this.mjData.qfrc_applied[i] += qfrc[i];
}
```

**Important Notes:** 
- The new API requires passing `model` and `mjData` as the first two parameters
- Force, torque, and point must be passed as **Float64Array** (TypedArrays), not regular JavaScript arrays
- The 7th parameter is `qfrc_target` which must be a Float64Array sized to `model.nv` (number of velocity dimensions)
- `model.nv` represents the number of degrees of freedom in velocity space
- **CRITICAL**: `mj_applyFT` only computes the generalized forces - you must add them to `mjData.qfrc_applied` to actually apply them to the simulation
- You need access to the `mujoco` instance (typically available via `this.runtime.mujoco` in managers)

### 5. Observation/Action Manager Parameter Mismatch

**Error:** `TypeError: Cannot read properties of undefined (reading 'qpos')`

**Cause:** Observation classes expecting `mjData` but receiving `simulation` (or vice versa during migration)

**Solution:** Ensure the entire chain passes `mjData`:
```javascript
// In ConfigObservationManager
async onPolicyLoaded({ config, model, mjData, assetMeta }) {  // ✅ Receives mjData
    this.observationGroups[key] = components.map(obsConfigItem => 
        this.createObservationInstance({
            obsConfig: obsConfigItem,
            model,
            mjData,  // ✅ Passes mjData
            assetMeta,
        })
    );
}

createObservationInstance({ obsConfig, model, mjData }) {  // ✅ Receives mjData
    return new ObsClass(model, mjData, this.runtime, kwargs);  // ✅ Passes mjData
}

// In observation class
constructor(model, mjData, runtime, kwargs = {}) {  // ✅ Receives mjData
    this.mjData = mjData;  // ✅ Stores as mjData
}

compute() {
    return this.mjData.qpos.subarray(...);  // ✅ Uses mjData
}
```

### 6. ONNX Policy Initialization Errors

**Error:** `TypeError: Cannot read properties of undefined (reading 'length')` in `onnxHelper.js`

**Cause:** ONNX session not properly initialized before inference

**Solution:** Add proper error handling and validation:
```javascript
// In ONNXModule constructor
constructor(config) {
    if (!config || !config.path || !config.meta) {
        throw new Error('ONNXModule config must have path and meta properties');
    }
    this.mjModelPath = config.path;
    this.metaData = config.meta;
    if (!this.metaData.in_keys) {
        throw new Error('ONNXModule meta must have in_keys property');
    }
    this.isRecurrent = config.meta.in_keys.includes("adapt_hx");
}

async init() {
    try {
        const modelResponse = await fetch(this.mjModelPath);
        if (!modelResponse.ok) {
            throw new Error(`Failed to fetch model: ${modelResponse.status}`);
        }
        const modelArrayBuffer = await modelResponse.arrayBuffer();
        
        this.inKeys = this.metaData["in_keys"];
        this.outKeys = this.metaData["out_keys"];
        
        this.session = await ort.InferenceSession.create(modelArrayBuffer, {
            executionProviders: ['wasm'],
            graphOptimizationLevel: 'all'
        });
    } catch (error) {
        console.error('[ONNXModule] Failed to initialize:', error);
        throw error;
    }
}

async runInference(input) {
    if (!this.inKeys || !this.session) {
        throw new Error('ONNXModule not properly initialized');
    }
    // ... inference code
}
```

### 7. Variable Scope in Try-Catch Blocks

**Error:** `ReferenceError: config is not defined`

**Cause:** Variable declared with `const` inside try block, then used outside

**Solution:** Declare variable before try block:
```javascript
// ❌ Wrong
try {
    const config = await response.json();
    // ... initialization
} catch (error) {
    throw error;
}
// config not accessible here
if (manager) {
    await manager.onPolicyLoaded({ config });  // ❌ Error!
}

// ✅ Correct
let config;
try {
    config = await response.json();
    // ... initialization
} catch (error) {
    throw error;
}
// config accessible here
if (manager) {
    await manager.onPolicyLoaded({ config });  // ✅ Works!
}
```

## Migration Checklist

Use this checklist when migrating a file:

### Per File:
- [ ] Update `Model.load_from_xml()` → `MjModel.loadFromXML()`
- [ ] Update `new State()` and `new Simulation()` → `new MjData()`
- [ ] Replace all `simulation.method()` → `mujoco.mj_method(model, data)`
- [ ] Replace all `model.property()` → `model.property` (remove parentheses)
- [ ] Replace all `data.property()` → `data.property` (remove parentheses)
- [ ] Update `model.getOptions()` → `model.opt`
- [ ] Update `.free()` → `.delete()`
- [ ] Add null checks for optional properties (lights, etc.)

### For Classes:
- [ ] Update constructor signature: `simulation` → `mjData`
- [ ] Update stored references: `this.simulation` → `this.mjData`
- [ ] Update all data access: `this.simulation.qpos` → `this.mjData.qpos`
- [ ] Update callback signatures to receive `mjData`
- [ ] Update all places that pass parameters to other classes

### For Manager Coordinators:
- [ ] Update `onPolicyLoaded` to receive `mjData`
- [ ] Update `onSceneLoaded` to receive `mjData`
- [ ] Update calls to `createObservationInstance` to pass `mjData`
- [ ] Update instantiation of observation classes to pass `mjData`

## Testing After Migration

Verify these behaviors after completing the migration:

- [ ] **Model Loading**: Scene loads without "is not a function" errors
- [ ] **Simulation Steps**: Simulation advances without crashes
- [ ] **Robot Visualization**: Visual representation updates correctly
- [ ] **Policy Inference**: ONNX policy loads and runs without errors
- [ ] **Observations**: All observation components compute correctly
- [ ] **Actions**: Robot responds to control inputs
- [ ] **Reset Functionality**: Scene can be reset without issues
- [ ] **Memory Cleanup**: No console warnings about memory leaks
- [ ] **Manager Lifecycle**: All manager callbacks execute without errors
- [ ] **Error Handling**: Helpful error messages appear for actual problems

## Additional Resources

### Official Documentation
- [MuJoCo Documentation](https://mujoco.readthedocs.io/)
- [MuJoCo WASM Repository](https://github.com/google-deepmind/mujoco)

### Reference Implementation
- Check `src/mujoco_wasm/examples/demoapp.ts` in the official MuJoCo WASM repository for the canonical usage patterns of the 3.3.7 API

### Key Takeaways

1. **Direct Property Access**: This is the #1 source of migration errors. Every property uses direct access - no exceptions.
2. **Unified Data Structure**: `MjData` replaces both `State` and `Simulation` - simpler and more aligned with C++ API
3. **Parameter Chain**: When migrating, update the entire parameter chain from runtime → managers → observation classes
4. **Error Messages**: The new API provides clearer error messages, but you need proper validation to catch initialization failures
5. **Type Consistency**: Be consistent with parameter names (`mjData` everywhere, not mixing `data`, `mjData`, `simulation`)
