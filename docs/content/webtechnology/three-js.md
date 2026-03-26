---
title: Three Js
created: 2026-03-26 12:35:19 +0100
last_modified: 2026-03-26 13:50:13 +0100
---

# Reference Code 

## Geometry 

### Icosphere (bal)
```javascript
const geo = new THREE.IcosahedronGeometry(1, 2);
```

## Materials

### Basis (geen shading, alleen kleur)
```javascript
const mat = new THREE.MeshBasicMaterial({ color: 0xccff })
```

### Standaard (licht en schaduw, maar geen reflecties)
```javascript
const mat = new THREE.MeshStandardMaterial({ 
	color: 0xffffff,
	flatShading: true // true: geen gladde overgangen tussen vlakken, false: gladde schaduw
}) 
```

### Wireframe (alleen lijnen, geen vlakken)
```javascript
const wireMaterial = new THREE.MeshBasicMaterial({
	color: 0xffffff,
	wireframe: true
});
```

## Animatie

### Rotatie
```javascript
mesh.rotation.y = t * 0.0001;
```

### Scaling loop
```javascript
mesh.scale.setScalar(Math.cos(t * 0.001) + 1.0);
```

# Tutorial 

[Video Tutorial](https://www.youtube.com/watch?v=UMqNHi1GDAE)

## Opdracht 1: Wireframe Ball Challenges 

### Startcode

```html 
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Getting Started with Three.js</title>
    <style>
      body {
        margin: 0;
      }
    </style>
    <script type="importmap">
			{
				"imports": {
					"three": "https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.module.js",
          			"jsm/": "https://cdn.jsdelivr.net/npm/three@0.161.0/examples/jsm/"
        		}
			}
		</script>
  </head>
  <body>
    <script type="module" src="index.js"></script>
  </body>
</html>
```

```javascript 
// Import the Three.js library
import * as THREE from 'three'; 
import { OrbitControls } from "jsm/controls/OrbitControls.js";

// Maak het HTML object aan waarnaar we zullen renderen
const w = window.innerWidth;
const h = window.innerHeight;
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(w, h);
document.body.appendChild(renderer.domElement);

// Maak een camera
const fov = 75;
const aspect = w / h;
const near = 0.1;
const far = 10;
const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
camera.position.z = 2;

// Maak een scene
const scene = new THREE.Scene();

// Voeg controls toe zodat we kunnen rondkijken met de muis
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; // Voegt een beetje traagheid toe aan de controls
controls.dampingFactor = 0.05; // Hoeveel traagheid

// Maak een 3D vorm
const geo = new THREE.IcosahedronGeometry(1, 2);

// Material: standaard (licht en schaduw, maar geen reflecties)
const mat = new THREE.MeshStandardMaterial({ 
	color: 0xffffff,
	flatShading: true // true: geen gladde overgangen tussen vlakken, false: gladde schaduw
}) 

// Maak een mesh aan door de 3D vorm en het materiaal te combineren
const mesh = new THREE.Mesh(geo, mat);
scene.add(mesh);

// Materiaal: wireframe (alleen lijnen, geen vlakken)
const wireMaterial = new THREE.MeshBasicMaterial({
	color: 0xffffff,
	wireframe: true
});

// Voeg het wireframe materiaal toe aan dezelfde mesh
const wireframe = new THREE.Mesh(geo, wireMaterial);
wireframe.scale.setScalar(1.001); // Maak het wireframe iets groter zodat het niet precies op de vlakken ligt
mesh.add(wireframe);

// Licht
const hemiLight = new THREE.HemisphereLight(0x0099ff, 0xaa5500, 1);
scene.add(hemiLight);

// Maak een animatielus
function animate(t = 0) {
	console.log(t);

	// Vraag de browser om de volgende frame te renderen
	requestAnimationFrame(animate);

	// Pas de scale van het object aan volgens de cosinus van de tijd
	//mesh.scale.setScalar(Math.cos(t * 0.001) + 1.0);
	controls.update(); // Update de controls (voor de damping)
}
animate();

	// Rotatie animatie
	mesh.rotation.y = t * 0.0001;

	// Render de scene met de camera
	renderer.render(scene, camera);

```

### Niveau 1: Kleine aanpassingen

1. Verander de kleur van het object.
2. Geef de wireframe een andere kleur.
3. Laat het object draaien rond een andere as (of meerdere asses)
4. Pas de snelheid van de rotatie aan.
5. Verander de positie van de camera.

### Niveau 2: Combineren 

1. Voeg een tweede mesh toe.
2. Geef het een andere animatie.
