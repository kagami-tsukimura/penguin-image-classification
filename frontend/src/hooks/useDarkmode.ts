import { useCallback, useEffect, useState } from 'react';

type UseDarkMode = (isDark?: boolean) => {
  isDarkMode: boolean;
  toggle: (isDark?: boolean) => void;
};

export const useDarkMode: UseDarkMode = (isInitialDark = false) => {
  const [isDarkMode, setIsDarkMode] = useState<boolean>(isInitialDark);
  const toggle = useCallback(
    (isDark?: boolean | ((prevState: boolean) => boolean)) => {
      typeof isDark === 'undefined'
        ? setIsDarkMode((state) => !state)
        : setIsDarkMode(isDark);
    },
    []
  );

  useEffect(() => {
    isDarkMode
      ? document.documentElement.classList.add('dark')
      : document.documentElement.classList.remove('dark');
  }, [isDarkMode]);

  return { isDarkMode, toggle };
};
