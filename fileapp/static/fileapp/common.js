window.history.scrollRestoration = 'manual'

const colors = ['red', 'blue', 'yellow', 'black']
const searchParams = new URLSearchParams(location.search);
let color;

if (searchParams.has("color")) color = searchParams.get("color");
else color = colors[Math.floor(Math.random() * colors.length)];

document.documentElement.style.setProperty('--color1', `var(--${color}-color1)`);
document.documentElement.style.setProperty('--color2', `var(--${color}-color2)`);
document.documentElement.style.setProperty('--color2-act', `var(--${color}-color2-act)`);
document.documentElement.style.setProperty('--color3', `var(--${color}-color3)`);
document.documentElement.style.setProperty('--color4', `var(--${color}-color4)`);