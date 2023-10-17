import React from 'react';
import { MdDarkMode, MdLightMode } from 'react-icons/md';
import { useDarkMode } from '../hooks/useDarkmode';

const DarkModeButton: React.FC = () => {
  const { isDarkMode, toggle } = useDarkMode();

  return (
    <div className='pr-12'>
      <button
        title='Change Mode'
        onClick={() => toggle()}
        className='w-12 h-6 rounded-full p-1 bg-gray-400 dark:bg-gray-600 relative transition-colors duration-500 ease-in focus:outline-none focus:ring-2 focus:ring-blue-700 dark:focus:ring-blue-600 focus:border-transparent '
      >
        <div className='flex items-center justify-center'>
          {isDarkMode ? (
            <div title='Change Light Mode' className='ml-6'>
              <MdDarkMode />
            </div>
          ) : (
            <div title='Change Dark Mode' className='mr-6'>
              <MdLightMode />
            </div>
          )}
        </div>
      </button>
    </div>
  );
};

export default DarkModeButton;
