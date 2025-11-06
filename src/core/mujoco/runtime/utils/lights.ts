import * as THREE from 'three';
import type { MjModel } from 'mujoco-js';

interface CreateLightsParams {
  mujoco: any; // MuJoCo instance
  mjModel: MjModel;
  mujocoRoot: THREE.Group;
  bodies: Record<number, THREE.Group>;
}

export function createLights({ mujoco, mjModel, mujocoRoot, bodies }: CreateLightsParams): THREE.Light[] {
  const lights: THREE.Light[] = [];
  let ambientSum = new THREE.Color(0, 0, 0);

  // Process model lights
  if (mjModel.nlight > 0) {
    for (let l = 0; l < mjModel.nlight; l++) {
      if (!mjModel.light_active[l]) continue;

      const lightType = mjModel.light_type[l];
      let light: THREE.DirectionalLight | THREE.PointLight | THREE.SpotLight;

      if (lightType === mujoco.mjtLightType.mjLIGHT_DIRECTIONAL.value) {
        light = new THREE.DirectionalLight();
      } else if (lightType === mujoco.mjtLightType.mjLIGHT_POINT.value) {
        light = new THREE.PointLight();
      } else if (lightType === mujoco.mjtLightType.mjLIGHT_SPOT.value) {
        light = new THREE.SpotLight();
      } else if (lightType === mujoco.mjtLightType.mjLIGHT_IMAGE.value) {
        console.warn(`Skipping unsupported light type: mjLIGHT_IMAGE (light index ${l})`);
        continue;
      } else {
        console.warn(`Skipping unknown light type: ${lightType} (light index ${l})`);
        continue;
      }

      // Colors: Combine diffuse and specular; add ambient to sum
      const diffuseColor = new THREE.Color().fromArray(mjModel.light_diffuse.slice(l * 3, l * 3 + 3));
      const specularColor = new THREE.Color().fromArray(mjModel.light_specular.slice(l * 3, l * 3 + 3));
      light.color = diffuseColor.clone().add(specularColor);
      light.intensity = mjModel.light_intensity[l] || 1;

      const ambientColor = new THREE.Color().fromArray(mjModel.light_ambient.slice(l * 3, l * 3 + 3));
      ambientSum.add(ambientColor);

      // Shadow properties
      light.castShadow = mjModel.light_castshadow[l];
      if (light.castShadow) {
        light.shadow!.mapSize.width = 1024;
        light.shadow!.mapSize.height = 1024;
        light.shadow!.camera.near = 1;
        light.shadow!.camera.far = 10;
        light.shadow!.radius = mjModel.light_bulbradius[l] * 50; // Arbitrary scale for softness
      }

      // Position and direction (static; in full sim, update via mjData.light_xpos/light_xdir)
      const pos = mjModel.light_pos.slice(l * 3, l * 3 + 3);
      const dir = mjModel.light_dir.slice(l * 3, l * 3 + 3);
      if (lightType === mujoco.mjtLightType.mjLIGHT_DIRECTIONAL.value) {
        light.position.set(0, 0, 0);
        light.target.position.set(dir[0], dir[1], dir[2]);
      } else {
        light.position.set(pos[0], pos[1], pos[2]);
        if (lightType === mujoco.mjtLightType.mjLIGHT_SPOT.value) {
          light.target.position.set(pos[0] + dir[0], pos[1] + dir[1], pos[2] + dir[2]);
        }
      }

      // Spot-specific properties
      if (lightType === mujoco.mjtLightType.mjLIGHT_SPOT.value) {
        light.angle = mjModel.light_cutoff[l] * Math.PI / 180;
        const exponent = mjModel.light_exponent[l];
        (light as THREE.SpotLight).penumbra = 1 / (1 + exponent); // Higher exponent -> sharper
      }

      // Attenuation and range (non-directional only)
      if (lightType !== mujoco.mjtLightType.mjLIGHT_DIRECTIONAL.value) {
        const att = mjModel.light_attenuation.slice(l * 3, l * 3 + 3); // [constant, linear, quadratic]
        if (att[2] > 0) {
          light.decay = 2; // Quadratic
        } else if (att[1] > 0) {
          light.decay = 1; // Linear
        } else {
          light.decay = 0; // No decay
        }
        light.intensity /= att[0] || 1;
        light.distance = mjModel.light_range[l]; // Max distance
      }

      // Attach to parent body or root
      const bodyId = mjModel.light_bodyid[l];
      if (bodyId >= 0 && bodies[bodyId]) {
        bodies[bodyId].add(light);
      } else {
        mujocoRoot.add(light);
      }
      lights.push(light);
    }
  }

  // Handle headlight (if active)
  if (mujoco.mjVisual?.headlight?.active) {
    const headAmbient = new THREE.Color().fromArray(mujoco.mjVisual.headlight.ambient);
    ambientSum.add(headAmbient);

    const headDiffuse = new THREE.Color().fromArray(mujoco.mjVisual.headlight.diffuse);
    const headSpecular = new THREE.Color().fromArray(mujoco.mjVisual.headlight.specular);
    const headLight = new THREE.DirectionalLight();
    headLight.color = headDiffuse.clone().add(headSpecular);
    headLight.intensity = 1;

    // Shadows
    headLight.castShadow = true;
    headLight.shadow!.mapSize.width = 1024;
    headLight.shadow!.mapSize.height = 1024;
    headLight.shadow!.camera.near = 1;
    headLight.shadow!.camera.far = 10;
    headLight.shadow!.radius = 0;

    // Position (camera-relative; approximate for static)
    headLight.position.set(0, 0, 10);
    headLight.target.position.set(0, 0, 0);

    mujocoRoot.add(headLight);
    lights.push(headLight);
  }

  // Add combined ambient light
  if (!ambientSum.equals(new THREE.Color(0, 0, 0))) {
    const ambientLight = new THREE.AmbientLight(ambientSum, 0.2);
    mujocoRoot.add(ambientLight);
    lights.push(ambientLight);
  }

  // Fallback default light
  if (lights.length === 0) {
    const defaultLight = new THREE.DirectionalLight();
    mujocoRoot.add(defaultLight);
    lights.push(defaultLight);
  }

  return lights;
}
