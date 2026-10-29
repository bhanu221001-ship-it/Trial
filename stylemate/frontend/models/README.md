# Fitting-room avatar models

Put `.glb` files in this folder (`stylemate/frontend/models/`). The fitting room
finds them by itself: there is no code to edit.

| File here | Shown when Body model is |
|---|---|
| `male_base.glb` | Male |
| `female_base.glb` | Female |

## Adding a model

1. Export it from Blender (or anything else) as **glTF Binary (.glb)**, Y-up,
   in metres, standing on the ground, facing forward (+Z). This is Blender's default.
2. Name it so the category is in the name, then copy it here:
   - `female_<anything>.glb` (also `woman`, `girl`): a Female model
   - `male_<anything>.glb` (also `man`, `boy`): a Male model
   - any other name: offered under both Male and Female

   "female" is checked first, so `female_slim.glb` is never read as male.
3. Open the fitting room. Locally the new file shows up on the next page load,
   with no restart. On Render, commit and push; it arrives with the deploy.

The fitting room lists every model for the current **Body model** under
**Model**, plus **Basic** (the avatar built from your measurements). Each person's
choice is remembered in their browser. With no choice saved, it shows the
category's model marked `"default": true`, else its first model alphabetically.

## Optional: models.json

Only needed to set a display name, force a category, pick a default, or turn a
model that does not face forward. Files not listed still work.

```json
{"models": [
  {"file": "female_curvy.glb", "name": "Female curvy", "category": "female", "default": true},
  {"file": "avatar_x.glb", "category": "male", "rotationY": 180}
]}
```

`rotationY` is in degrees. A broken `models.json` is reported and ignored.

## What is checked

`GET /api/models` reads this folder on every request and offers only files that:
- have a real GLB 2.0 header whose length matches the file;
- have a JSON chunk that parses and contains at least one mesh;
- are no larger than 80 MB;
- need no Draco, Meshopt or KTX2/Basis decoder (none is set up);
- have every external `.bin` or image file they refer to present (embedded ones are best).

Anything else is listed under `errors` with the reason, and named in the
fitting room, but never loaded. A model that still fails in the browser, for
example a 404, a corrupt file or odd dimensions, leaves the Basic avatar on screen
with a message.

## How a model is shown

- **Viewer:** the same 3D viewer, camera, lights, controls and fit reports as
  before.
- **Clothes:** fitted to the model itself, from each item's size chart at the
  size chosen (see below). With **Basic** chosen, the earlier measurement shells
  are shown.
- **Materials:** kept exactly as authored. Nothing is tinted, and the skin colour
  read from an uploaded photo is not applied to GLB models.
- **Size:** scaled uniformly to the avatar's height from the measurements,
  centred, with feet on the floor.

## How clothes are fitted to a model

Each garment is built from the model's own skin, using its skeleton's skin
weights to tell torso, arm, hand, leg, foot and neck apart:

- **Upper half** (T-shirts, tops, shirts, kurtas, dresses, jackets): from the
  base of the neck down by the chart length. Sleeves run the chart sleeve length
  along the arm from the top of the shoulder. A sleeve longer than the arm
  continues past the wrist by the difference, over the hand. A sleeveless top's
  armholes sit at the chart's shoulder width.
- **Lower half** (jeans, trousers, shorts): a mid-rise waistband, legs to the
  chart inseam below the crotch (shorts: 20 cm at most).
- **Long pieces** (kurtas, dresses, skirts, long tops) hang as one piece around
  both legs below the hip joints, widening a little toward the hem.
- **Shoes:** a smooth shell over each foot below the ankle.
- **How loose:** the chart girth at the size chosen minus your measurement,
  added to the model's body. A top with no waist size falls straight from the
  chest. Cloth spans hollows (between the breasts, along the spine) and is
  smoothed over small bumps.
- **Layers:** shoes, then trousers and skirts, then tops, kurtas and dresses,
  then jackets. Each is kept outside the ones beneath it, so a kurta covers
  the jeans' waistband.

Changing an item's size in the fitting room refits it.

The model needs the MakeHuman/MPFB skeleton these two files use (bones such as
`neck01`, `upperarm01.L`, `wrist.L`, `upperleg01.L`, `foot.L`, `spine01`).
For a model without it, the clothes fall back to the measurement shells and
the fitting room says why.

## Limitations

- **Body shape does not follow measurements.** These files have no morph targets,
  so only overall height adapts; chest, waist and hips are the model's own. The
  fit report still uses your measurements.
- **It is a shape, not a cloth simulation.** There are no folds, and the cloth
  does not move. The garment's girth is your looseness added to the model's
  body, so how loose it looks matches the fit report, not the chart's
  centimetres on this body.
- **The model stands in its A-pose,** so a sleeve longer than the arm follows
  the hand, and the hand shows past the end of the sleeve.
- **No animations.** A model's animations are not played.
- **The sidebar's small turning mannequin** still uses the Basic avatar. Only the
  fitting room changed.
- **Download size:** each model is downloaded the first time it is shown (about
  4.5 MB for the two here), then kept in memory. Up to four are kept; older ones
  are freed.
