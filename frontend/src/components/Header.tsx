import React from 'react';
import { GiPenguin } from 'react-icons/gi';

const Header: React.FC = () => {
  return (
    <header className='py-2'>
      <div className='container mx-auto flex justify-between items-center px-2 w-full'>
        <div className='text-3xl font-bold'>
          <a href='#top' className='text-cyan-200 flex items-center'>
            ペンギンの分類
            <GiPenguin />
          </a>
        </div>
      </div>
    </header>
  );
};

export default Header;
