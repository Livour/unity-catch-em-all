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
