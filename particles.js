// document.addEventListener("DOMContentLoaded", () => {
//     const container = document.querySelector(".container");
//     const numParticles = 200; // Adjust the number of particles as desired
  
//     // Generate particles
//     for (let i = 0; i < numParticles; i++) {
//       const particle = document.createElement("div");
//       particle.classList.add("particle");
//       container.appendChild(particle);
//       positionParticle(particle);
//       animateParticle(particle);
//     }
  
//     function positionParticle(particle) {
//       const x = Math.random() * document.documentElement.clientWidth; // Set initial x position within the document width
//       const y = Math.random() * document.documentElement.clientHeight; // Set initial y position within the document height
//       particle.style.setProperty("--translate-x", `${x}px`);
//       particle.style.setProperty("--translate-y", `${y}px`);
//     }
  
//     function animateParticle(particle) {
//       const duration = Math.random() * 10 + 5; // Randomize duration between 5 and 15 seconds
//       particle.style.animationDuration = `${duration}s`;
//     }
//   });
  