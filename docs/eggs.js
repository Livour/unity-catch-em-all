function makeEgg(mob, unknown) {
  const e = document.createElement("span");
  e.className = "egg" + (unknown ? " unknown" : "");
  e.style.setProperty("--base", mob.egg[0]);
  e.style.setProperty("--spot", mob.egg[1]);
  e.setAttribute("aria-hidden", "true");
  return e;
}
