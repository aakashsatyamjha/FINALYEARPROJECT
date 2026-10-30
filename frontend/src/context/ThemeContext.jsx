import React, { createContext, useContext, useEffect, useState } from 'react';

const ThemeContext = createContext({
  theme: 'light',
  resolvedTheme: 'light',
  setTheme: () => {},
});

export function ThemeProvider({ children }) {
  const [theme, setThemeState] = useState('light');
  const [resolvedTheme, setResolvedTheme] = useState('light');

  useEffect(() => {
    // Force light mode — remove any cached dark preference
    try { localStorage.removeItem('foodguard-theme'); } catch (_) {}

    const root = document.documentElement;
    root.classList.add('light');
    root.classList.remove('dark');
    root.style.colorScheme = 'light';
    setResolvedTheme('light');
  }, [theme]);

  const setTheme = (newTheme) => {
    setThemeState(newTheme);
  };

  return (
    <ThemeContext.Provider value={{ theme, resolvedTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
