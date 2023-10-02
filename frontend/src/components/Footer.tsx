import { SiQiita } from 'react-icons/si';

const Footer: React.FC = () => {
  return (
    <footer className='mt-auto w-full max-w-[85rem] py-10 px-4 sm:px-6 lg:px-8 mx-auto'>
      {/* <!-- Grid --> */}
      <div className='text-center'>
        <div>
          <a
            className='flex-none text-xl font-semibold text-cyan-600 dark:text-cyan-200'
            href='#'
            aria-label='Brand'
          >
            ペンギンの分類
          </a>
        </div>
        {/* <!-- End Col --> */}

        <div className='mt-3'>
          <p className='text-gray-500'>
            We're part of the{' '}
            <a
              className='font-semibold text-blue-600 hover:text-blue-700 dark:text-blue-500 dark:hover:text-blue-400'
              href='https://kagami-portfolio.netlify.app/'
            >
              Kagami.com
            </a>{' '}
            family.
          </p>
          <p className='text-gray-500'>© 2023 Kagami Tsukimura</p>
        </div>

        {/* <!-- Social Brands --> */}
        <div className='mt-3 space-x-2'>
          <a className='icon' href='mailto:kagami.penguin.t@gmail.com'>
            <svg
              className='w-3.5 h-3.5'
              xmlns='http://www.w3.org/2000/svg'
              width='16'
              height='16'
              fill='currentColor'
              viewBox='0 0 16 16'
            >
              <path d='M15.545 6.558a9.42 9.42 0 0 1 .139 1.626c0 2.434-.87 4.492-2.384 5.885h.002C11.978 15.292 10.158 16 8 16A8 8 0 1 1 8 0a7.689 7.689 0 0 1 5.352 2.082l-2.284 2.284A4.347 4.347 0 0 0 8 3.166c-2.087 0-3.86 1.408-4.492 3.304a4.792 4.792 0 0 0 0 3.063h.003c.635 1.893 2.405 3.301 4.492 3.301 1.078 0 2.004-.276 2.722-.764h-.003a3.702 3.702 0 0 0 1.599-2.431H8v-3.08h7.545z' />
            </svg>
          </a>
          <a className='icon' href='https://twitter.com/tukimurakagami'>
            <svg
              className='w-3.5 h-3.5'
              xmlns='http://www.w3.org/2000/svg'
              width='16'
              height='16'
              fill='currentColor'
              viewBox='0 0 16 16'
            >
              <path d='M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865l8.875 11.633Z' />
            </svg>
          </a>
          <a className='icon' href='https://github.com/kagami-tsukimura'>
            <svg
              className='w-3.5 h-3.5'
              xmlns='http://www.w3.org/2000/svg'
              width='16'
              height='16'
              fill='currentColor'
              viewBox='0 0 16 16'
            >
              <path d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z' />
            </svg>
          </a>
          <a className='icon' href='https://qiita.com/kagami_t'>
            <SiQiita />
          </a>
        </div>
        {/* <!-- End Social Brands --> */}
      </div>
      {/* <!-- End Grid --> */}
    </footer>
  );
};

export default Footer;
