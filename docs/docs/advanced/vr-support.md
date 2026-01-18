# VR Support

Enable virtual reality viewing for your Muwanx simulations using WebXR.

## Overview

Muwanx includes built-in support for VR viewing through WebXR, allowing users to experience simulations in immersive virtual reality.

## Browser Support

VR support requires:

- **Chrome/Edge**: Version 79+ with WebXR enabled
- **Firefox**: Version 98+ with WebXR support
- **Oculus Browser**: Native support on Quest devices
- **Safari**: Limited support (iOS WebXR is experimental)

## VR Devices

Compatible with:

- Meta Quest (1, 2, 3, Pro)
- HTC Vive
- Valve Index
- Windows Mixed Reality headsets
- Any WebXR-compatible device

## Enabling VR

VR support is automatically available in all Muwanx applications. No special configuration needed:

```python
import muwanx as mwx

builder = mwx.Builder()
project = builder.add_project(name="VR Demo")
project.add_scene(model=model, name="My Scene")

# VR button appears automatically in the UI
app = builder.build()
app.launch()
```

## Using VR Mode

### On Desktop

1. Connect your VR headset
2. Open the Muwanx application in a WebXR-compatible browser
3. Click the VR button in the UI
4. Put on your headset

### On Quest

1. Open Oculus Browser
2. Navigate to your Muwanx application URL
3. Tap the VR button
4. The view transitions to immersive VR

## VR Controls

### Head Tracking

- Look around naturally with head movement
- 6DOF (six degrees of freedom) tracking supported

### Controller Input

- **Thumbsticks**: Move camera position
- **Grip buttons**: Interact with objects (if enabled)
- **Triggers**: Apply forces (if enabled)
- **A/B buttons**: UI interaction

## VR-Optimized Scenes

### Performance Considerations

VR requires higher frame rates (90 FPS minimum). Optimize for VR:

```python
# Keep models simple for VR
model = mujoco.MjModel.from_xml_string("""
<mujoco>
  <option timestep="0.01"/>  <!-- Adjust timestep for performance -->
  <visual>
    <global offwidth="2048" offheight="2048"/>  <!-- VR resolution -->
  </visual>

  <worldbody>
    <!-- Use simple geometries -->
    <geom type="plane" size="10 10 0.1"/>

    <!-- Avoid excessive contacts -->
    <body pos="0 0 1">
      <joint type="free"/>
      <geom type="box" size="0.2 0.2 0.2"/>
    </body>
  </worldbody>
</mujoco>
""")
```

### Scale and Positioning

Position objects at comfortable viewing distances:

```python
# Good for VR - objects at appropriate scale
model = mujoco.MjModel.from_xml_string("""
<mujoco>
  <worldbody>
    <geom type="plane" size="5 5 0.1"/>

    <!-- Position at comfortable viewing height -->
    <body pos="0 2 1">  <!-- 2m forward, 1m up -->
      <joint type="free"/>
      <geom type="box" size="0.1 0.1 0.1"/>
    </body>
  </worldbody>
</mujoco>
""")
```

## VR-Specific Features

### Stereo Rendering

Muwanx automatically enables stereo rendering in VR mode:

- Separate views for each eye
- Proper 3D depth perception
- IPD (interpupillary distance) adjustment

### Room-Scale VR

For devices with room-scale tracking:

```python
# Create a larger environment for room-scale
model = mujoco.MjModel.from_xml_string("""
<mujoco>
  <worldbody>
    <!-- Large play area -->
    <geom type="plane" size="10 10 0.1"/>

    <!-- Obstacles at room scale -->
    <body pos="1 0 0.5">
      <geom type="box" size="0.2 0.2 0.5"/>
    </body>

    <body pos="-1 0 0.5">
      <geom type="cylinder" size="0.15 0.5"/>
    </body>
  </worldbody>
</mujoco>
""")
```

## Testing VR

### Desktop Testing

Test VR without a headset using browser dev tools:

**Chrome:**

1. Open DevTools (F12)
2. Click menu (⋮) → More tools → WebXR
3. Enable "Emulate VR device"
4. Click VR button in your app

### Mobile Testing

Test on mobile before deploying to VR:

1. Deploy to a test URL
2. Access from mobile browser
3. Check performance and controls
4. Optimize as needed

## Example: VR-Optimized Demo

```python
"""VR Demo - Optimized for Virtual Reality"""

import mujoco
import muwanx as mwx


def create_vr_scene():
    """Create a scene optimized for VR viewing."""
    model = mujoco.MjModel.from_xml_string("""
    <mujoco model="vr_demo">
      <option timestep="0.01" gravity="0 0 -9.81"/>

      <visual>
        <global offwidth="2048" offheight="2048"/>
        <quality shadowsize="4096"/>
      </visual>

      <asset>
        <texture name="grid" type="2d" builtin="checker"
                 width="512" height="512" rgb1="0.2 0.2 0.2"
                 rgb2="0.3 0.3 0.3"/>
        <material name="grid_mat" texture="grid"
                  texrepeat="10 10" reflectance="0.1"/>
      </asset>

      <worldbody>
        <!-- Textured ground -->
        <geom type="plane" size="10 10 0.1" material="grid_mat"/>

        <!-- Ambient lighting -->
        <light pos="0 0 5" dir="0 0 -1" diffuse="0.8 0.8 0.8"/>
        <light pos="3 3 3" dir="-1 -1 -1" diffuse="0.5 0.5 0.5"/>

        <!-- Robot at comfortable viewing distance -->
        <body pos="0 2 1" euler="0 0 0">
          <freejoint/>

          <!-- Body -->
          <geom type="box" size="0.15 0.1 0.2" rgba="0.7 0.7 0.9 1"/>

          <!-- Head -->
          <body pos="0 0 0.3">
            <geom type="sphere" size="0.1" rgba="0.9 0.9 0.7 1"/>
          </body>

          <!-- Arms -->
          <body pos="0.15 0 0.1">
            <joint type="hinge" axis="0 1 0" range="-90 90"/>
            <geom type="capsule" size="0.03" fromto="0 0 0 0 0 -0.3"
                  rgba="0.7 0.7 0.9 1"/>
          </body>

          <body pos="-0.15 0 0.1">
            <joint type="hinge" axis="0 1 0" range="-90 90"/>
            <geom type="capsule" size="0.03" fromto="0 0 0 0 0 -0.3"
                  rgba="0.7 0.7 0.9 1"/>
          </body>

          <!-- Legs -->
          <body pos="0.07 0 -0.2">
            <joint type="hinge" axis="1 0 0" range="-120 30"/>
            <geom type="capsule" size="0.04" fromto="0 0 0 0 0 -0.4"
                  rgba="0.7 0.7 0.9 1"/>
          </body>

          <body pos="-0.07 0 -0.2">
            <joint type="hinge" axis="1 0 0" range="-120 30"/>
            <geom type="capsule" size="0.04" fromto="0 0 0 0 0 -0.4"
                  rgba="0.7 0.7 0.9 1"/>
          </body>
        </body>

        <!-- Interactive objects around the space -->
        <body pos="1 1.5 0.5">
          <joint type="free"/>
          <geom type="sphere" size="0.1" rgba="1 0.3 0.3 1"/>
        </body>

        <body pos="-1 1.5 0.5">
          <joint type="free"/>
          <geom type="box" size="0.08 0.08 0.08" rgba="0.3 1 0.3 1"/>
        </body>
      </worldbody>
    </mujoco>
    """)

    return model


def main():
    builder = mwx.Builder()
    vr_project = builder.add_project(name="VR Experience")

    # Create VR-optimized scene
    vr_model = create_vr_scene()
    vr_project.add_scene(
        model=vr_model,
        name="VR Demo",
        initial_qpos={}
    )

    # Build and launch
    app = builder.build()
    print("Open this application in a VR browser and click the VR button!")
    app.launch()


if __name__ == "__main__":
    main()
```

## Performance Tips

### Reduce Complexity

- Use simple collision geometries
- Limit the number of contacts
- Reduce mesh polygon counts

### Optimize Rendering

```xml
<visual>
  <!-- Reduce shadow quality if needed -->
  <quality shadowsize="2048"/>

  <!-- Adjust texture resolution -->
  <global offwidth="1024" offheight="1024"/>
</visual>
```

### Adjust Timestep

```xml
<option timestep="0.01"/>  <!-- Larger timestep = better performance -->
```

## Troubleshooting

### VR Button Not Appearing

- Check browser WebXR support
- Ensure HTTPS connection (required for WebXR)
- Verify VR device is connected

### Poor Performance

- Reduce model complexity
- Lower texture resolution
- Simplify collision meshes
- Increase simulation timestep

### Tracking Issues

- Ensure good lighting in room
- Check device batteries
- Recalibrate headset
- Restart VR device

### Nausea/Discomfort

- Ensure 90+ FPS
- Avoid rapid camera movements
- Add comfort vignette (handled by browser)
- Keep simulation smooth and stable

## Best Practices

1. **Test Early**: Test VR mode during development
2. **Optimize for Performance**: Target 90 FPS minimum
3. **Appropriate Scale**: Use real-world scales
4. **Comfortable Viewing**: Position objects 1-3m away
5. **Smooth Motion**: Avoid jerky movements
6. **Clear UI**: Make controls obvious
7. **Progressive Enhancement**: Ensure desktop experience works well too

## WebXR Resources

- [WebXR Specification](https://www.w3.org/TR/webxr/)
- [WebXR Device API](https://immersive-web.github.io/webxr/)
- [Can I Use WebXR](https://caniuse.com/webxr)

## See Also

- [Creating Scenes](../user-guide/creating-scenes.md) - Scene basics
- [Deployment](deployment.md) - Deploy VR applications
- [Building Projects](../user-guide/building-projects.md) - Build and optimization
