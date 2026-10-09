export const themes = [
  { id: "light", label: "☀️ Light" },
  { id: "dark", label: "🌙 Dark" },
  { id: "oled", label: "⚫ OLED" },
  { id: "forest", label: "🌿 Forest" },
  { id: "ocean", label: "🌊 Ocean" },
];

const THEME_KEY = "theme";

export function getTheme() {
  const theme = localStorage.getItem(THEME_KEY);


  if (!theme) {
    return "light";
  }

  if (themes.some(item => item.id === theme)) {
    return theme;
  }

  return "light";
}

export function setTheme(theme: string) {
  document.documentElement.setAttribute("data-theme", theme);

  localStorage.setItem(THEME_KEY, theme);
}