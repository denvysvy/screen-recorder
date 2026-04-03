let startX, startY
let selecting = false

const overlay = document.getElementById("overlay");
overlay.focus();

const box = document.getElementById("selection");

overlay.addEventListener("mousedown", e => {

  const rect = overlay.getBoundingClientRect()

  selecting = true
  startX = e.clientX - rect.left
  startY = e.clientY - rect.top

  box.style.left = startX + "px"
  box.style.top = startY + "px"
  box.style.width = "0px"
  box.style.height = "0px"
  box.style.display = "block"
})

overlay.addEventListener("mousemove", e => {

  if (!selecting) return

  const rect = overlay.getBoundingClientRect()

  const currentX = e.clientX - rect.left
  const currentY = e.clientY - rect.top

  const width = Math.abs(currentX - startX)
  const height = Math.abs(currentY - startY)

  box.style.width = width + "px"
  box.style.height = height + "px"

  box.style.left = Math.min(startX, currentX) + "px"
  box.style.top = Math.min(startY, currentY) + "px"
})

overlay.addEventListener("mouseup", async e => {

  selecting = false;

  const scale = window.devicePixelRatio;

  const area = {
    top: Math.round(Math.min(startY, e.clientY) * scale),
    left: Math.round(Math.min(startX, e.clientX) * scale),
    width: Math.round(Math.abs(e.clientX - startX) * scale),
    height: Math.round(Math.abs(e.clientY - startY) * scale)
  };

  await window.pywebview.api.set_capture_area(area);
  window.pywebview.api.close_selector();
});

document.addEventListener("keydown", e => {
  if (e.key === "Escape") {
    window.pywebview.api.close_selector()
  }
})