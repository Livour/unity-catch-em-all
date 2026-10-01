// Display name: English first, Hebrew in brackets. Wrap in dir="ltr" so it reads left to right on RTL pages.
function label(mob) {
  return `${mob.en} (${mob.he})`;
}

// Mob picture: silhouette until caught, full color after.
function makeMob(mob, unknown) {
  const img = document.createElement("img");
  img.className = "mob" + (unknown ? " unknown" : "");
  img.src = `mobs/${mob.id}.webp`;
  img.alt = "";
  img.loading = "lazy";
  img.decoding = "async";
  img.setAttribute("aria-hidden", "true");
  return img;
}

// Pokeball, 12x12 pixel art drawn from scratch. K outline, R red, D red shade, H shine, W white, G white shade.
const BALL = ["....KKKK....", "..KKRRRRKK..", ".KRRRRRRHRK.", ".KRRRRRRRRK.", "KDRRRKKRRRDK", "KKKKKWWKKKKK",
  "KWWWWKKWWWWK", "KWWWWWWWWWGK", ".KWWWWWWWGK.", ".KGWWWWWGGK.", "..KKGGGGKK..", "....KKKK...."];
const COL = { K: "#000", R: "#e3262e", D: "#a5121a", H: "#ff9a9a", W: "#fff", G: "#b8b8b8" };
const BALL_SVG = '<svg viewBox="0 0 12 12" width="100%" height="100%" shape-rendering="crispEdges" aria-hidden="true">' +
  BALL.flatMap((row, y) => [...row].map((c, x) => COL[c] ? `<rect x="${x}" y="${y}" width="1" height="1" fill="${COL[c]}"/>` : "")).join("") + "</svg>";
