import { useState } from "react";

import { getTheme, setTheme, themes } from "@/utils/theme/theme";

export function ThemeSwitcher() {
  const [theme, setCurrentTheme] = useState(getTheme());

  function handleChange(event: React.ChangeEvent<HTMLSelectElement>) {
    const value = event.target.value;

    setCurrentTheme(value);
    setTheme(value);
  }

  return (
    <select
      value={theme}
      onChange={handleChange}
      className="rounded border px-3 py-2"
    >
      {themes.map((theme) => (
        <option key={theme.id} value={theme.id}>
          {theme.label}
        </option>
      ))}
    </select>
  );
}